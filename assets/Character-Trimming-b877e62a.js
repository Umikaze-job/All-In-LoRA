import{T as C}from"./template01-a006ca31.js";import{m as $}from"./mini-Button01-afe0a576.js";import{d as h,b as d,_ as g,o as n,g as r,F as c,i as I,e as a,n as p,t as N,h as x,r as i,c as y,w as m,a as B,f as u}from"./index-b77c9346.js";const L=h({props:{addClass:String,subItems:Array,nowId:Number,paths:Array},methods:{getTextClass(t){return t==this.nowId?"bg-NormalButtonColor p-1 rounded-sm":"p-1 rounded-sm"},mouseEnterItem(t){const e=t.target;e.children[0].classList.add("left-0"),e.children[0].classList.remove("right-0"),d({targets:e.children[0],width:"100%",easing:"easeOutExpo",duration:300})},mouseLeaveItem(t){const e=t.target;e.children[0].classList.remove("left-0"),e.children[0].classList.add("right-0"),d({targets:e.children[0],width:"0",easing:"easeOutExpo",duration:300})},gotoPath(t){const e=this.paths[t];this.$router.push({name:e})}}}),k=["onClick"],T=a("div",{class:"w-0 h-full absolute bg-NormalButtonHover top-0 left-0 z-[-1]"},null,-1),V={key:0,class:"bg-white w-[2px] h-[80%]"};function E(t,e,f,b,_,w){return n(),r("div",{class:p("text-white font-Raleway text-xl flex flex-row justify-start gap-3 items-center select-none "+t.addClass)},[(n(!0),r(c,null,I(t.subItems,(l,s)=>(n(),r(c,{key:s},[a("div",{class:"relative",onMouseenter:e[0]||(e[0]=(...o)=>t.mouseEnterItem&&t.mouseEnterItem(...o)),onMouseleave:e[1]||(e[1]=(...o)=>t.mouseLeaveItem&&t.mouseLeaveItem(...o)),onClick:o=>t.gotoPath(s)},[T,a("p",{class:p(t.getTextClass(s))},N(l),3)],40,k),s!=t.subItems.length-1?(n(),r("div",V)):x("",!0)],64))),128))],2)}const S=g(L,[["render",E]]),F=h({setup(){},components:{"base-tem":C,"mini-button":$,"button-set":S},data(){return{pathName:["ct-trimming-setting","ct-select-files","ct-output-folder"]}},computed:{getSubPageId(){const t=this.$route.name;return this.pathName.indexOf(t)}}}),O={class:"flex flex-row text-center text-lg text-white font-Raleway"},P={class:"basis-1/2 flex flex-row justify-end"};function R(t,e,f,b,_,w){const l=i("button-set"),s=i("mini-button"),o=i("RouterView"),v=i("base-tem");return n(),y(v,null,{maintitle:m(()=>[B("Manipulating Images")]),buttonContents:m(()=>[a("div",O,[u(l,{paths:t.pathName,"now-id":t.getSubPageId,"add-class":"basis-1/2","sub-items":["Setting","Files","Output Folder"]},null,8,["paths","now-id"]),a("div",P,[u(s,{addClass:"ml-2",buttonName:"Trimming","button-color-hover":"bg-ApplyColor"})])])]),mainContents:m(()=>[u(o,{name:"subView"})]),_:1})}const z=g(F,[["render",R]]);export{z as default};
