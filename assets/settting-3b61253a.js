import{f as h}from"./form-dropdown01-421352ae.js";import{T as v}from"./template01-92276447.js";import{d as g,q as i,M as b,_ as w,r as x,o as l,k as _,w as c,f as A,h as n,c as p,i as M,n as d,t as C,F as k}from"./index-09c46877.js";const E=g({setup(){const{itemMouseEnter:e,itemMouseLeave:t,itemMouseEnter02:s,itemMouseLeave02:o}=b();return{itemMouseEnter:e,itemMouseLeave:t,itemMouseEnter02:s,itemMouseLeave02:o}},data(){return{buttonData:[{name:"test01",isActive:!1},{name:"test02",isActive:!1},{name:"test03",isActive:!1}]}},methods:{buttonitemTextStyle(e){return e?"text-slate-700":"text-white"},changeIsActive(e,t){this.buttonData.forEach((s,o)=>{if(o==t&&!s.isActive){const a=e.target.parentNode.children[o].children[1];s.isActive=!0,i.set(a,{width:"100%"}),i({targets:a,duration:300,height:["0%","100%"],easing:"easeOutExpo"})}else if(o!=t&&s.isActive){const a=e.target.parentNode.children[o].children[1];s.isActive=!1,i({targets:a,duration:300,height:["100%","0%"],width:"0%",easing:"easeOutExpo"})}})}},components:{"base-tem":v,"drop-form01":h}}),B={class:"flex flex-row gap-2 min-h-[100px]"},y={class:"basis-1/4 border-winBorder border-white rounded-md p-3 flex flex-col text-white text-xl font-Raleway text-center gap-4"},D=["onClick"],T=n("div",{class:d("absolute bg-white bottom-0 z-[-2] h-[1px] pointer-events-none")},null,-1),$=n("div",{class:d("absolute bg-white bottom-0 left-0 z-[-1] h-[0%] w-full pointer-events-none")},null,-1),L=n("div",{class:"basis-3/4 border-winBorder border-white rounded-md grid grid-cols-3 gap-2 p-3"},null,-1);function N(e,t,s,o,a,S){const f=x("base-tem");return l(),_(f,null,{maintitle:c(()=>[A("Setting")]),buttonContents:c(()=>[]),mainContents:c(()=>[n("div",B,[n("div",y,[(l(!0),p(k,null,M(e.buttonData,(u,m)=>(l(),p("div",{key:m,onClick:r=>e.changeIsActive(r,m),onMouseenter:t[0]||(t[0]=r=>e.itemMouseEnter(r)),onMouseleave:t[1]||(t[1]=r=>e.itemMouseLeave(r)),class:"relative w-[90%] mx-auto cursor-pointer"},[T,$,n("p",{class:d(`w-full text-center ${e.buttonitemTextStyle(u.isActive)} pointer-events-none select-none`)},C(u.name),3)],40,D))),128))]),L])]),_:1})}const O=w(E,[["render",N]]);export{O as default};
