import{d as o,A as n,_ as a,o as l,g as i,e,s,t as r}from"./index-b77c9346.js";const c=o({setup(){},data(){return{store:n()}},computed:{getSelectingFolderName(){return this.store.getSelectingFolderName==""?"None":this.store.getSelectingFolderName}}}),d={class:"container mx-auto"},m={class:"flex flex-row mx-12 mt-3"},_={class:"basis-1/2"},p={class:"font-Raleway text-white text-2xl text-left underline underline-offset-4"},f={class:"basis-1/2"},h={class:"font-Raleway text-white text-2xl text-right"},u={class:"mx-3 mt-3 w-full"},x={class:"mx-3 mt-2 w-full min-h-[200px]"};function g(t,S,w,$,v,N){return l(),i("div",d,[e("div",m,[e("div",_,[e("p",p,[s(t.$slots,"maintitle")])]),e("div",f,[e("p",h,r("Selecting Folder: "+t.getSelectingFolderName),1)])]),e("div",u,[s(t.$slots,"buttonContents")]),e("div",x,[s(t.$slots,"mainContents")])])}const b=a(c,[["render",g]]);export{b as T};
