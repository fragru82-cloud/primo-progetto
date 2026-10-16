"""Sofia Voce - sintesi con voce clonata + controllo pronuncia.

Per ogni frase genera fino a MAX_TENTATIVI versioni, le ritrascrive con Whisper
e tiene quella con meno errori. Poi unisce le frasi, accelera leggermente
(senza alterare il timbro) ed esporta in OGG/Opus per WhatsApp/Telegram.
"""
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import jiwer
import torch
import torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from faster_whisper import WhisperModel
from num2words import num2words

MAX_TENTATIVI = 5
VELOCITA = 1.15          # +15%
PAUSA_S = 0.25           # pausa tra frasi
PARAMS = dict(exaggeration=0.5, cfg_weight=0.4, temperature=0.6)

# Correzioni di pronuncia: testo scritto -> come deve leggerlo il motore.
LESSICO = {
    r"\bPEC\b": "pec",
    r"\bErre Di\b": "Erre Dì",
    r"\bripetermelo\b": "ripetermi il numero",
}


def normalizza_per_sintesi(testo):
    for pat, sost in LESSICO.items():
        testo = re.sub(pat, sost, testo, flags=re.IGNORECASE)
    return testo


# Parole che Whisper trascrive "a modo suo" anche se pronunciate bene.
ALIAS_ASR = {r"global ?(inc|link|ink)": "globalink", r"\bpack\b|\bpeck\b": "pec",
             r"\baloha\b|\balo è\b": "aloe", r"\be-mail\b": "email",
             r"\bil re di\b|\bere di\b": "erre dì", r"\berre di\b": "erre dì"}


def per_confronto(testo):
    testo = re.sub(r"\d+", lambda m: " " + num2words(int(m.group()), lang="it") + " ", testo)
    testo = testo.lower().replace("'", " ").replace("’", " ")
    for pat, sost in ALIAS_ASR.items():
        testo = re.sub(pat, sost, testo)
    testo = re.sub(r"[^\wàèéìòù ]", " ", testo)
    return re.sub(r"\s+", " ", testo).strip()


def frasi(testo):
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+", testo) if f.strip()]


class SofiaVoce:
    def __init__(self, riferimento, device="cpu"):
        torch.set_num_threads(4)
        self.ref = riferimento
        self.tts = ChatterboxMultilingualTTS.from_pretrained(device=device)
        self.asr = WhisperModel("medium", device=device, compute_type="int8")
        self.sr = self.tts.sr

    def _errore(self, wav, atteso):
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            torchaudio.save(tmp.name, wav, self.sr)
            segs, _ = self.asr.transcribe(tmp.name, language="it")
            sentito = " ".join(s.text for s in segs)
        a, h = per_confronto(atteso), per_confronto(sentito)
        out = jiwer.process_words(a, h)
        diff = []
        for al in out.alignments[0]:
            if al.type != "equal":
                diff.append(" ".join(out.references[0][al.ref_start_idx:al.ref_end_idx]) + " -> " +
                            " ".join(out.hypotheses[0][al.hyp_start_idx:al.hyp_end_idx]))
        return out.wer, "; ".join(diff) or "tutto corretto"

    def frase(self, testo):
        da_leggere = normalizza_per_sintesi(testo)
        migliore = None
        for _ in range(MAX_TENTATIVI):
            wav = self.tts.generate(da_leggere, language_id="it", audio_prompt_path=self.ref, **PARAMS)
            err, sentito = self._errore(wav, da_leggere)
            if migliore is None or err < migliore[0]:
                migliore = (err, wav, sentito)
            if err == 0:
                break
        return migliore

    def sintetizza(self, testo, out_ogg):
        pezzi, report = [], []
        silenzio = torch.zeros(1, int(self.sr * PAUSA_S))
        for f in frasi(testo):
            err, wav, sentito = self.frase(f)
            pezzi += [wav, silenzio]
            report.append((round(err, 2), f, sentito.strip()))
        audio = torch.cat(pezzi[:-1], dim=1)
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            torchaudio.save(tmp.name, audio, self.sr)
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", tmp.name,
                            "-af", f"atempo={VELOCITA}", "-c:a", "libopus", "-b:a", "32k",
                            "-ac", "1", "-ar", "48000", "-application", "voip", out_ogg], check=True)
        return report


if __name__ == "__main__":
    ref, outdir = sys.argv[1], Path(sys.argv[2])
    testi = [
        "Buongiorno, Globalink, sono Sofia. Il signor Aloe in questo momento è in riunione: posso prendere un messaggio o preferisce essere richiamato più tardi?",
        "Perfetto, allora le confermo il ritiro della merce per martedì ventitré, tra le nove e le undici. Le mando subito la conferma via email.",
        "Mi scusi, non ho capito bene il numero dell'ordine. Può ripetermelo lentamente, per favore? Così verifico la spedizione e le dico a che punto è.",
        "Francesco, è arrivata una PEC dall'Agenzia delle Entrate per Erre Di. Non è urgente, però c'è una scadenza tra quindici giorni: vuoi che la giri al commercialista?",
    ]
    sv = SofiaVoce(ref)
    for i, t in enumerate(testi, 1):
        t0 = time.time()
        rep = sv.sintetizza(t, str(outdir / f"sofia_frase{i}.ogg"))
        print(f"## frase {i} ({round(time.time() - t0)} s)", flush=True)
        for err, f, sentito in rep:
            print(f"  errore {err} | sentito: {sentito}", flush=True)
