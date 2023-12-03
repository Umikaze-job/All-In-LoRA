import{T as v}from"./template01-8903d691.js";import{B as $}from"./mini-Button01-f65293f1.js";import{d as h,f as d,_ as g,o as n,g as r,F as c,h as I,n as p,b as a,t as N,i as x,r as i,c as y,w as u,a as B,e as l}from"./index-8f2ce7ae.js";const L=h({props:{addClass:String,subItems:Array,nowId:Number,paths:Array},methods:{getTextClass(t){return t==this.nowId?"bg-NormalButtonColor p-1 rounded-sm":"p-1 rounded-sm"},mouseEnterItem(t){const e=t.target;e.children[0].classList.add("left-0"),e.children[0].classList.remove("right-0"),d({targets:e.children[0],width:"100%",easing:"easeOutExpo",duration:300})},mouseLeaveItem(t){const e=t.target;e.children[0].classList.remove("left-0"),e.children[0].classList.add("right-0"),d({targets:e.children[0],width:"0",easing:"easeOutExpo",duration:300})},gotoPath(t){const e=this.paths[t];this.$router.push({name:e})}}}),T=["onClick"],k=a("div",{class:"w-0 h-full absolute bg-NormalButtonHover top-0 left-0 z-[-1]"},null,-1),S={key:0,class:"bg-white w-[2px] h-[80%]"};function V(t,e,f,b,_,w){return n(),r("div",{class:p("text-white font-Raleway text-xl flex flex-row justify-start gap-3 items-center select-none "+t.addClass)},[(n(!0),r(c,null,I(t.subItems,(m,s)=>(n(),r(c,{key:s},[a("div",{class:"relative",onMouseenter:e[0]||(e[0]=(...o)=>t.mouseEnterItem&&t.mouseEnterItem(...o)),onMouseleave:e[1]||(e[1]=(...o)=>t.mouseLeaveItem&&t.mouseLeaveItem(...o)),onClick:o=>t.gotoPath(s)},[k,a("p",{class:p(t.getTextClass(s))},N(m),3)],40,T),s!=t.subItems.length-1?(n(),r("div",S)):x("",!0)],64))),128))],2)}const E=g(L,[["render",V]]),O=h({setup(){},components:{"base-tem":v,"mini-button":$,"button-set":E},data(){return{pathName:["ct-trimming-setting","ct-select-files","ct-output-folder"]}},computed:{getSubPageId(){const t=this.$route.name;return this.pathName.indexOf(t)}}}),F={class:"flex flex-row text-center text-lg text-white font-Raleway"},P={class:"basis-1/2 flex flex-row justify-end"};function R(t,e,f,b,_,w){const m=i("button-set"),s=i("mini-button"),o=i("RouterView"),C=i("base-tem");return n(),y(C,null,{maintitle:u(()=>[B("Character Trimming")]),buttonContents:u(()=>[a("div",F,[l(m,{paths:t.pathName,"now-id":t.getSubPageId,"add-class":"basis-1/2","sub-items":["Trimming Setting","Select Files","Output Folder"]},null,8,["paths","now-id"]),a("div",P,[l(s,{buttonName:"Open"}),l(s,{addClass:"ml-2",buttonName:"Delete"})])])]),mainContents:u(()=>[l(o,{name:"subView"})]),_:1})}const D=g(O,[["render",R]]);export{D as default};