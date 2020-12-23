const hourHand = document.querySelector("#hour");
const minuteHand = document.querySelector("#minute");
const secondHand = document.querySelector("#second");

let hrPosition=20;
let minPosition=130;
let secPosition=267;

hourHand.style.transform="rotate("+hrPosition+"deg)"
minuteHand.style.transform="rotate("+minPosition+"deg)"
secondHand.style.transform="rotate("+secPosition+"deg)"