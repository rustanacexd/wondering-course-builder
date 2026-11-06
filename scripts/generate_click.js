// Start generating one Wondering lesson. Run with Claude in Chrome's javascript_tool on the course page
// (https://wondering.app/?project=<courseId>), right after navigating there. Replace __SID__ with the
// lesson's sessionId (from insert_lesson / the replacements file). Navigate back to the course page before
// every lesson: a click that opens a lesson instead of the dialog breaks a loop over one page.
// Returns CREATING (started), LIMIT (daily cap hit), NO NODE / NO BUTTON (page changed), or OK <path>.
const sid = '__SID__';
const w = ms => new Promise(r => setTimeout(r, ms));
let n = null;
for (let i = 0; i < 40 && !n; i++) { n = document.querySelector(`[data-lesson-session-id="${sid}"]`); if (!n) await w(500); }
if (!n) { 'NO NODE' } else {
  (n.querySelector('div[role=button]') || n).click();
  let b = null;
  for (let i = 0; i < 30 && !b; i++) { b = [...document.querySelectorAll('button')].find(x => /start reading/i.test(x.textContent)); if (!b) await w(300); }
  if (!b) { 'NO BUTTON' } else {
    b.click(); await w(3000);
    const t = document.body.innerText;
    /limit/i.test(t) ? 'LIMIT' : (/creating|generating/i.test(t) ? 'CREATING' : 'OK ' + location.pathname)
  }
}
