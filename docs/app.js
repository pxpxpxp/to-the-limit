'use strict';
const modes=[{rate:'7.159',divider:'6',fill:'66.67%',note:'Off: stock high-speed CPU timing. This is the core default.'},{rate:'8.591',divider:'5',fill:'80%',note:'+20% mode: eligible cycles use 5 master clocks. Memory waits still apply.'},{rate:'10.739',divider:'4',fill:'100%',note:'+50% mode: eligible cycles use 4 master clocks. Memory waits still apply.'}];
const controls=document.querySelectorAll('[data-mode]');
controls.forEach(button=>button.addEventListener('click',()=>{const mode=modes[Number(button.dataset.mode)];controls.forEach(control=>control.setAttribute('aria-pressed',String(control===button)));document.querySelector('#frequency').textContent=mode.rate;document.querySelector('#divisor').textContent=mode.divider;document.querySelector('#meter-fill').style.width=mode.fill;document.querySelector('#mode-note').textContent=mode.note;}));

// The original GIF stays intact. A still preview gives motion control and saves
// bandwidth until this card is in view; reduced-motion users opt in explicitly.
const rewindDemo=document.querySelector('#rewind-demo');
const rewindToggle=document.querySelector('.rewind-toggle');
if(rewindDemo&&rewindToggle){
  let playing=false;
  const setRewindPlayback=value=>{
    playing=value;
    rewindDemo.src=value?rewindDemo.dataset.animation:rewindDemo.dataset.poster;
    rewindToggle.setAttribute('aria-pressed',String(value));
    rewindToggle.textContent=value?'PAUSE REWIND GIF Ⅱ':'PLAY REWIND GIF ▶';
  };
  rewindToggle.hidden=false;
  rewindToggle.addEventListener('click',()=>setRewindPlayback(!playing));
  if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>{
      if(entries.some(entry=>entry.isIntersecting)){setRewindPlayback(true);observer.disconnect();}
    },{threshold:0.25});
    observer.observe(rewindDemo);
  }
}
