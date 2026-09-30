# #48 CHAT-BUBBLES · Messenger conversation

> A messenger panel slides in beside the person; a contact header, then messages pop from their tail corner with a spring, the other side shows bouncing typing dots first, sent messages get double ticks that turn blue when read, and the thread pushes up as it grows.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/chat-bubbles.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_CHAT-BUBBLES.mp4
> Runner: run_style CHAT-BUBBLES · Example: examples/chat-bubbles/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: social ads and UGC ("the text that started it"), dating/food/delivery apps, customer-support stories, short-form storytelling, WhatsApp-business promos.
- Avoid when: the conversation has more than ~6 messages in 10 s (unreadable), messages are longer than two lines, or the frame has no clean third.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#chat` | the panel: `rgba(233,226,216,.62)` (messenger wallpaper tone), blur 22 px + saturate 1.3, radius 34 px, shadow 0 30 80 | positioned by `area` (x, top, w, bottom) |
| `#hd` | contact header, 92% light grey: gradient avatar circle (62 px) with an initial, name (32 px), status in green (21 px) | |
| `#list` | the thread, bottom-anchored inside `#thread` (overflow hidden) | new rows push older ones up |
| `.bb.me` / `.bb.them` | bubbles: #d9fdd3 (me) / #ffffff (them), radius 22 px with a 6 px corner on the tail side, max-width 78% | pop from the tail corner (`transform-origin`) |
| `.meta` | time (17 px) + double-tick SVG on "me" bubbles | ticks grey → blue #53bdeb after `read` seconds |
| `.typing` | three 12 px grey dots in a "them" bubble | bounce for 0.9 s before each incoming message |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| panel (fade, y 40→0, scale .96→1) | contact.t | .70 | expo.out | to until | fade + y −30 at until−.45, .45 s | power3.in |
| typing dots (y −8 yoyo, 3 repeats, stagger .1) | message.t−.9 | .22 per bounce | sine.inOut | until the message | hidden | — |
| bubble (scale .3→1, fade) | message.t | .50 | back.out(2) | stays | — | — |
| meta (time + ticks) fade | message.t+.35 | .30 | — | — | — | — |
| ticks turn blue | message.t + read (1.2) | instant | — | — | — | — |
- Rhythm: 1.3–1.8 s between messages (sample 1.5, 2.9, 4.7, 6.1, 7.6, 8.9): enough to read a short line.
- Row visibility, typing indicators and tick colour are computed from video time in `onPlace` (seek-safe): rows are `display:none` until their time, so the bottom-anchored list "scrolls" naturally.
- The signature move: typing dots → spring pop from the tail corner → blue ticks. Three micro-beats that make it feel like a real chat.

## Typography
- Latin: Manrope 700 contact name (32 px), Manrope 500 message text (29 px, line-height 1.35), time 17 px.
- Hebrew: `pair: "secular"` (default): Secular One. **RTL messenger rule: outgoing ("me") bubbles sit on the LEFT, incoming on the right.** Under `direction: rtl` flexbox also mirrors `justify-content`, which put "me" on the wrong side in an earlier render, so the kit sets each row to `direction: ltr` and places bubbles by physical side, then sets the bubble text back to RTL.
- Mentions and handles (@name) inside Hebrew text need bidi isolation (`<bdi>` or `unicode-bidi: isolate`) or the @ jumps to the wrong end.
- Maximum copy: ≈ 30 characters per message (one line at 78% width); two lines maximum.

## Colour and surface
- Roles: `panel` rgba(233,226,216,.62), `me` #d9fdd3, `them` #ffffff, `text` #111b21, `tick` #53bdeb, `head` #f0f2f5 (the header CSS uses its own 92% grey).
- These are generic messenger tones drawn in CSS: no WhatsApp/iMessage logos. For an iMessage feel: `me: "#0a84ff"` with white text (edit `.bt` colour), `them: "#e9e9eb"`.

## Layout and safe zones (1920×1080 canvas)
- `area`: x 1120 (left edge), top 90, w 680, bottom 1000: nearly full height on the free side; keep x + w ≤ 1824 (5% margin).
- Industry convention: the viewer reads the conversation, so keep the panel on the side the person looks towards, or opposite their face.
- 9:16: x ≈ 60, w ≈ 960, top ≈ 240, bottom ≈ 1500 (on a 1080×1920 canvas the kit composes 1920×1080: render 16:9 and crop, or rebuild the canvas).

## What the footage must give you
- Shoot it like this: one take, 6–20 s, the person with a phone in one third (screen never visible), the rest soft and empty; locked-off, shallow depth of field.
- Tracking: none. Matte: not needed.
- Good footage: phone in hand on a sofa, at a café, walking slowly (locked-off). Bad: visible phone screen, a face under the panel, busy backgrounds.

## Build it
### A. With the kit
```bash
python scripts/run_style.py CHAT-BUBBLES --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| messages[] | {from "me"/"them", text, t, time} | required |
| contact | {name, status, initial, t} | {"name": "", "t": .4} |
| area | {x, top, w, bottom} | 1120, 90, 680, 1000 |
| read | seconds until a sent message's ticks turn blue | 1.2 |
| until | the panel leaves | none |
| language / pair | he/en; Hebrew pair | en / "secular" |
| fonts | override | Manrope 700 / 500 |
| colors | {panel, me, them, text, tick, head} | see above |
| sfx | pop for sent, ting for received, whoosh on the panel | true |
| music, music_vol, plate_vol, name | — | none, .5, .6 |
```json
{
 "clip": "clips/phone.mp4",
 "contact": {"name": "Maya", "status": "online", "initial": "M", "t": 0.5},
 "messages": [
  {"from": "them", "text": "Did you book the table?", "t": 1.5, "time": "20:41"},
  {"from": "me", "text": "Done. 8pm, window seat", "t": 3.0, "time": "20:41"},
  {"from": "them", "text": "You're the best", "t": 4.8, "time": "20:42"}
 ],
 "until": 9.6
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const M = [{t: 1.5, me: false}, {t: 3.0, me: true}], READ = 1.2;
tl.fromTo("#chat", {opacity: 0, y: 40, scale: .96}, {opacity: 1, y: 0, scale: 1, duration: .7, ease: "expo.out"}, .5);
M.forEach((m, i) => {
  tl.fromTo(`#b${i}`, {scale: .3, opacity: 0}, {scale: 1, opacity: 1, duration: .5, ease: "back.out(2)"}, m.t);   // origin = tail corner (CSS)
  if (!m.me) tl.to(`#ty${i} i`, {y: -8, duration: .22, yoyo: true, repeat: 3, ease: "sine.inOut", stagger: .1}, m.t - .9);
});
// visibility is state, not animation: derive it from time so seeking works
window.onPlace = (t) => M.forEach((m, i) => {
  document.getElementById("r" + i).style.display = t >= m.t ? "flex" : "none";
  if (!m.me) document.getElementById("ty" + i).style.display = t >= m.t - .9 && t < m.t ? "flex" : "none";
  else document.getElementById("tk" + i).style.color = t >= m.t + READ ? "#53bdeb" : "#8696a0";
});
```

## Adapting it to the user's project
- Content: the user's real dialogue, short lines, the product/offer lands in the last message.
- Language: Hebrew → `"language": "he"`; outgoing bubbles go left automatically; isolate @handles.
- Brand: bubble colours can take the brand; keep text dark on light bubbles.
- Vertical 9:16: see layout.
- Longer clips: the thread holds as many rows as fit; older ones scroll out of the top.

## Sound
- `ui_pop` (.45) on sent messages, `glass_ting` (.45) on received, `ui_whoosh` (.3) when the panel appears.

## Pitfalls and QA checklist
- [ ] Hebrew: "me" bubbles on the LEFT; each row `direction: ltr`, bubble text RTL.
- [ ] Typing dots show only in the 0.9 s before incoming messages.
- [ ] Each message has ≥ 1.3 s before the next (readable).
- [ ] @handles and numbers inside Hebrew bubbles are bidi-isolated.
- [ ] The panel doesn't cover the person's face at any frame.
