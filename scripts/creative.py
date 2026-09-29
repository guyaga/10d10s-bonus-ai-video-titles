"""Gemini as an outside creative director: watch a finished ad, propose an alternative take on titles + narration.
python creative.py <video.mp4> "<brief>" "<current titles/VO summary>" > out.json
"""
import os
import sys
import time

from google import genai
from google.genai import types

c = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
f = c.files.upload(file=sys.argv[1], config={"mime_type": "video/mp4"})
while (f := c.files.get(name=f.name)).state.name == "PROCESSING":
    time.sleep(4)
prompt = f"""You are an award-winning commercial creative director reviewing a finished 15-30 s ad (AI video + tracked motion graphics + voiceover).
Brief: {sys.argv[2]}
Current version: {sys.argv[3]}

Watch it frame by frame and propose ONE genuinely different, stronger creative take on the TITLES and the NARRATION (the footage stays the same).
Rules: premium and restrained (few, meaningful titles; no comic multi-colour); every title must be tied to a moment/object in the footage with a timestamp;
narration lines must fit the time before the next line (about 2.5 words per second); no real-brand names; English.
Return JSON:
{{"concept": "one line: the new idea / angle",
  "why_better": "one or two sentences",
  "titles": [{{"t": seconds, "end": seconds, "text": "...", "placement": "where on screen / which object", "style": "stomp|tag|counter|lockup"}}],
  "narration": [{{"start": seconds, "text": "...", "delivery": "short style note"}}],
  "voice": "one-line description of the ideal voice",
  "lockup": {{"brand": "...", "line": "..."}}}}"""
r = c.models.generate_content(model="gemini-3.7-flash", contents=[f, prompt],
                              config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.7))
print(r.text)
c.files.delete(name=f.name)
