import{T as i}from"./template01-a006ca31.js";import{d as n,_ as r,r as c,o as d,c as p,w as s,a as u,e as t}from"./index-b77c9346.js";const h=n({components:{"base-tem":i},data(){return{isMultipleChoice:!1}},methods:{MultipleButtonClick(e){this.isMultipleChoice?e.target.classList.replace("bg-amber-800","bg-transparent"):e.target.classList.replace("bg-transparent","bg-amber-800"),this.isMultipleChoice=!this.isMultipleChoice}}}),b=t("div",{class:"flex flex-row text-center text-lg text-white font-Raleway"},null,-1),_={class:"flex flex-row gap-2 min-h-[100px]"},f={class:"basis-1/2 flex flex-col gap-2"},g={class:"flex flex-row justify-start gap-2"},x=t("button",{class:"px-3 py-1 font-Raleway text-white text-lg border-2 border-white rounded-lg bg-transparent hover:bg-slate-500 transition-all"},"Select All",-1),m=t("div",{class:"border-2 border-white min-h-[100px] rounded-lg"},null,-1),w=t("div",{class:"basis-1/2 border-2 border-white rounded-lg"},null,-1);function C(e,o,v,M,k,y){const l=c("base-tem");return d(),p(l,null,{maintitle:s(()=>[u("Tag Editor")]),buttonContents:s(()=>[b]),mainContents:s(()=>[t("div",_,[t("div",f,[t("div",g,[x,t("button",{onClick:o[0]||(o[0]=(...a)=>e.MultipleButtonClick&&e.MultipleButtonClick(...a)),class:"px-3 py-1 font-Raleway text-white text-lg border-2 border-white rounded-lg bg-transparent hover:bg-slate-500 transition-all"},"multiple choice")]),m]),w])]),_:1})}const $=r(h,[["render",C]]);export{$ as default};
