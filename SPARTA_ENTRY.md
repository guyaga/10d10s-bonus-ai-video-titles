# Sparta bonus entry: AI Video Titles

key: bonus-ai-video-titles
category: bonus
name (he): כותרות ו-HUD לסרטוני AI
nameEn: AI Video Titles
service: Motion Graphics · Seedance 2.5 + HyperFrames
githubUrl: https://github.com/guyaga/10d10s-bonus-ai-video-titles
guideUrl: https://github.com/guyaga/10d10s-bonus-ai-video-titles#readme
hub: https://ai-video-titles-guyaga.netlify.app

## description (he)
כותרות בסגנון After Effects מעל סרטוני AI, בנויות כקוד. כותרות "סטומפ" ענקיות שנוחתות על הביט ורצות לצד הדוגמנית, טקסט שיושב מאחורי האובייקט, HUD הולוגרפי של קסדה עם עוזרת קולית, סטטיסטיקות ספורט בסגנון שידור, כותרות קינטיות בעברית ופסי "טייפ" שקריאים מעל כל רקע, כתוביות קריוקי, ספירה לאחור למבצע בזק ועולמות מעוצבים מאפס: מצלמה תרמית, זכוכית מגדלת של צורף, שרטוט של אדריכל, מגזין עיצוב וכרטיס הזמנה של מטבח.

Gemini ו-optical flow עוקבים אחרי כל אובייקט בסרטון פריים-אחר-פריים, הכותרות מתוזמנות לביט ולקול, HyperFrames מרנדר ל-MP4, ו-Gemini עושה בדיקת איכות עד שהסרטון מוכן. 22 סגנונות מוכנים, לכל אחד תצוגה חיה ושורת פרומפט להעתקה באתר הסגנונות. מומלץ עם Seedance 2.5 לסרטון עצמו. משלב את יום 2 (אנליזת וידאו) ויום 4 (יצירת וידאו). אפשר לנסות מיד בלי שום מפתח: קליפ דמו של 8 שניות עם המעקב, המוזיקה והצלילים מגיע עם הסקיל. אתר הסגנונות: ai-video-titles-guyaga.netlify.app

## installPrompt
Install the ai-video-titles skill from https://github.com/guyaga/10d10s-bonus-ai-video-titles by cloning it to ~/.claude/skills/ai-video-titles, running pip install -r requirements.txt in that folder, then run python scripts/doctor.py and tell me which pipeline steps are available to me (it checks ffmpeg, Node, HyperFrames, GEMINI_API_KEY, ELEVEN_API_KEY, KIE_API_KEY, OPENAI_API_KEY and the sibling skills). Finally render the included demo with cd examples/demo && python ../../scripts/run_style.py STOMP-ESCORT --spec spec.json --render and show me the video, then open https://ai-video-titles-guyaga.netlify.app so I can pick a style for my own video.
