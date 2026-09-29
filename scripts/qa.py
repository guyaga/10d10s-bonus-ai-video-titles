"""Gemini QA of a finished video: concrete, timestamped defects + a ship/fix verdict (JSON).
python qa.py video.mp4 "<what the video should show>"   (needs GEMINI_API_KEY)
Loop: fix every issue, re-render, re-run until verdict == "ship". Gemini cannot hear subtle mix problems reliably;
for music quality use librosa/spectral checks and your own ears."""
import os, sys, time, json
from google import genai
from google.genai import types
c = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
f = c.files.upload(file=sys.argv[1], config={"mime_type": "video/mp4"})
while (f := c.files.get(name=f.name)).state.name == "PROCESSING":
    time.sleep(4)
prompt = f"""You are a strict motion-graphics QA reviewer. This ad should show: {sys.argv[2]}
Watch frame by frame. Report ONLY concrete defects with MM:SS.ms timestamps:
- a callout, tag, box, ring or dot that is NOT on the object it labels (drifts, lags, points at the wrong thing)
- text cut off by the frame edge, text unreadable, text covering a face
- a title or number that contradicts what the voiceover says or what is shown
- spelling mistakes, overlapping graphics, a graphic appearing in the wrong shot
- audio: voice clipped, music drowning the voice, silence where there should be sound
Return JSON: {{"verdict":"ship"|"fix","issues":[{{"t":"MM:SS.ms","what":"...","fix":"..."}}]}}. If it is clean, return verdict ship with no issues."""
r = c.models.generate_content(model="gemini-3.7-flash", contents=[f, prompt],
                              config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0))
print(r.text)
c.files.delete(name=f.name)
