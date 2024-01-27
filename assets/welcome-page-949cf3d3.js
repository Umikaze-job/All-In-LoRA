var N=Object.defineProperty;var B=(e,o,t)=>o in e?N(e,o,{enumerable:!0,configurable:!0,writable:!0,value:t}):e[o]=t;var n=(e,o,t)=>(B(e,typeof o!="symbol"?o+"":o,t),t);import{g as h,A as m,d as U,m as $,a as A,b as E,_ as S,r as f,o as r,c,e as P,w as g,F as x,f as W,t as u,h as w,i as C,n as k,j as d,k as b,l as L,v as D}from"./index-09c46877.js";import{T as I}from"./template01-92276447.js";import{m as R}from"./mini-Button01-fadaf757.js";import{m as j}from"./modal-textform01-a307623e.js";import{f as F}from"./form-dropdown01-421352ae.js";import{m as H}from"./ModalItemComp-450d0411.js";/* empty css                       */class p{constructor(){n(this,"phase");n(this,"formValue");n(this,"errorid");n(this,"textColor");n(this,"formtype");n(this,"buttonName");n(this,"choices");this.phase=0,this.formValue="",this.errorid=0,this.textColor="text-white",this.formtype=0,this.buttonName="welcomePage.buttonName",this.choices=[]}changeText(o){switch(o){case 0:this.textColor="text-white";break;case 1:this.textColor="text-blue-400";break;case 2:this.textColor="text-rose-400";case 3:this.textColor="text-yellow-400"}}async init(o){}async isClicked(o){}async UseAxois(o,t){}}class z extends p{constructor(){super();n(this,"title");n(this,"contents");this.title="welcomePage.welcome.title",this.contents="welcomePage.welcome.contents"}}class K extends p{constructor(){super();n(this,"title");n(this,"contents");this.title="welcomePage.sdmodel.title",this.contents="welcomePage.sdmodel.contents",this.phase=1,this.formtype=1}async init(t){await this.UseAxois("",t)}async isClicked(t){if(this.formValue==""){this.contents="welcomePage.form01.NoWords",this.changeText(2);return}await this.UseAxois(this.formValue,t)}async UseAxois(t,s){const a=await s.post(h()+"/api/welcome-page/sd-models-folder",{folder_path:t});if(a.data.error!=null){m().setErrorMessage(a.data.error);return}a.data.isfolder?a.data.modelCount==0?(this.contents="welcomePage.sdmodel.nomodels",this.changeText(2),this.phase=2):(this.contents="welcomePage.sdmodel.already",this.changeText(1),this.phase=2):(this.contents="welcomePage.form01.notalready",this.changeText(0),this.phase=1)}}class q extends p{constructor(){super();n(this,"title");n(this,"contents");this.title="welcomePage.sdscripts.title",this.contents="welcomePage.sdscripts.contents",this.phase=1,this.formtype=1}async init(t){await this.UseAxois("",t)}async isClicked(t){if(this.formValue==""){this.contents="welcomePage.form01.NoWords",this.changeText(2);return}await this.UseAxois(this.formValue,t)}async UseAxois(t,s){const a=await s.post(h()+"/api/welcome-page/kohyass-folder",{folder_path:t});if(a.data.error!=null){m().setErrorMessage(a.data.error);return}a.data.isfolder!=null&&!a.data.isfolder?(this.contents="welcomePage.form01.notalready",this.changeText(0),this.phase=1):a.data.notrain!=null&&!a.data.notrain?(this.contents="welcomePage.sdscripts.notrain",this.changeText(3),this.phase=2):a.data.nosdxl!=null&&!a.data.nosdxl?(this.contents="welcomePage.sdscripts.sdxl",this.changeText(3),this.phase=2):(this.contents="welcomePage.form01.already",this.changeText(1),this.phase=2)}}class G extends p{constructor(){super();n(this,"title");n(this,"contents");this.title="welcomePage.lorafolder.title",this.contents="welcomePage.lorafolder.contents",this.phase=1,this.formtype=1}async init(t){await this.UseAxois("",t)}async isClicked(t){if(this.formValue==""){this.contents="welcomePage.form01.NoWords",this.changeText(2);return}await this.UseAxois(this.formValue,t)}async UseAxois(t,s){const a=await s.post(h()+"/api/welcome-page/lora-folder",{folder_path:t});if(a.data.error!=null){m().setErrorMessage(a.data.error);return}a.data.isfolder?(this.contents="welcomePage.form01.already",this.changeText(1),this.phase=2):(this.contents="welcomePage.form01.notalready",this.changeText(0),this.phase=1)}}class J extends p{constructor(){super();n(this,"title");n(this,"contents");this.title="welcomePage.settingMixedPrecision.title",this.contents="welcomePage.settingMixedPrecision.contents",this.buttonName="welcomePage.settingMixedPrecision.buttonName",this.phase=1,this.formtype=3,this.choices=["fp16","bf16"]}async init(t){const s=await t.post(h()+"/api/welcome-page/setting-mixed-precision",{isInit:!0});s.data.error!=null?m().setErrorMessage(s.data.error):s.data.result!="no"&&(this.phase=2,this.changeText(1),this.contents="welcomePage.settingMixedPrecision.isSelected")}async isClicked(t){const s=await t.post(h()+"/api/welcome-page/setting-mixed-precision",{isInit:!1,value:this.formValue});s.data.error!=null?m().setErrorMessage(s.data.error):s.data.result!="no"&&(this.phase=2,this.changeText(1),this.contents="welcomePage.settingMixedPrecision.isSelected")}}class O extends p{constructor(){super();n(this,"title");n(this,"contents");this.title="welcomePage.checkCudaCudnn.title",this.contents="welcomePage.checkCudaCudnn.contents",this.buttonName="welcomePage.checkCudaCudnn.buttonName",this.phase=1,this.formtype=2}async init(t){await this.execute(t)}async isClicked(t){await this.execute(t)}async execute(t){const s=await t.post(h()+"/api/welcome-page/check-cuda-cudnn");s.data.error!=null?m().setErrorMessage(s.data.error):s.data.result=="nocuda"?(this.phase=1,this.changeText(2),this.contents="welcomePage.checkCudaCudnn.nocuda"):s.data.result=="nocudnn"?(this.phase=1,this.changeText(2),this.contents="welcomePage.checkCudaCudnn.nocudnn"):(this.phase=2,this.changeText(1),this.contents="welcomePage.checkCudaCudnn.isChecked")}}const Q=U({setup(e,o){const{isModal:t,canModalCancel:s,canControl:a}=H();return{isModal:t,canModalCancel:s,canControl:a}},data(){return{window_data:[new z,new O,new K,new q,new G,new J],store:m()}},methods:{async WindowButtonClicked(e){this.canControl(!1),this.isModal=!0,await e.isClicked(this.axios),this.canControl(!0),this.isModal=!1},async openExplorer(e){await this.axios.post(h()+"/api/welcome-page/open-explorer",{folder_name:e})}},computed:{canMakeLoRa(){return this.window_data.every(e=>e.phase==0||e.phase==2)}},watch:{canMakeLoRa:{handler:function(e){this.store.setCanMakeLoRa(e)},immediate:!0}},async created(){this.window_data.forEach(e=>{e.init(this.axios)})},components:{"base-tem":I,"mini-button":R,"modal-base":$,"modal-button":A,"modal-form":j,"modal-window":E,"form-dropdown01":F}}),X={id:"contentstyle01",class:"flex flex-col text-white font-Raleway flex-wrap w-full place-content-start"},Y={key:0,class:"border-winBorder border-white bg-NormalButtonColor rounded-md m-2 p-2 flex flex-col gap-2"},Z={class:"text-lg text-center"},ee=["onUpdate:modelValue"],te={key:3,class:"w-full flex justify-center"},oe=["onClick"],se={key:4,class:"w-full flex justify-center"},ae=["onClick"],ne=w("p",{class:"text-center text-xl underline decoration-myUnderLine01 py-8"},"Loading...",-1);function ie(e,o,t,s,a,re){const _=f("modal-form"),v=f("base-tem"),M=f("modal-window"),T=f("modal-base");return r(),c(x,null,[P(v,null,{maintitle:g(()=>[W(u(e.$t("topbar.SettingWindow.welcomePage")),1)]),mainContents:g(()=>[w("div",X,[(r(!0),c(x,null,C(e.window_data,(i,V)=>(r(),c("div",{key:V,class:"2xl:w-1/4 xl:w-1/3 md:w-1/2 p-2"},[i.phase!=-1?(r(),c("div",Y,[w("p",Z,u(e.$t(i.title)),1),i.contents!=null?(r(!0),c(x,{key:0},C(e.$t(i.contents).split(`
`),(l,y)=>(r(),c("p",{key:y,class:k(`text-md ${i.textColor}`)},u(l),3))),128)):d("",!0),i.formtype==1?(r(),b(_,{key:1,modelValue:i.formValue,"onUpdate:modelValue":l=>i.formValue=l},null,8,["modelValue","onUpdate:modelValue"])):d("",!0),i.formtype==3?L((r(),c("select",{key:2,"onUpdate:modelValue":l=>i.formValue=l,class:"border-white focus:border-white outline-none focus:ring-transparent transition-colors bg-NormalButtonColor rounded-md w-[90%] mx-auto"},[(r(!0),c(x,null,C(i.choices,(l,y)=>(r(),c("option",{key:y},u(l),1))),128))],8,ee)),[[D,i.formValue]]):d("",!0),[1,2,3].includes(i.formtype)?(r(),c("div",te,[w("button",{onClick:l=>e.WindowButtonClicked(i),class:k("border-winBorder border-white px-4 py-2 rounded-md bg-NormalButtonColor hover:bg-NormalButtonHover transition-colors")},u(e.$t(i.buttonName)),9,oe)])):d("",!0),i.formtype==1&&i.phase==2?(r(),c("div",se,[w("button",{onClick:l=>e.openExplorer(i.title),class:k("border-winBorder border-white px-4 py-2 rounded-md bg-NormalButtonColor hover:bg-NormalButtonHover transition-colors")},u(e.$t("welcomePage.openExplorer")),9,ae)])):d("",!0)])):d("",!0)]))),128))])]),_:1}),P(T,{"is-window":e.isModal,onModalCancel:o[0]||(o[0]=i=>e.isModal=!1),"can-background-cancel":e.canModalCancel},{default:g(()=>[e.store.getTransState==1?(r(),b(M,{key:0},{default:g(()=>[ne]),_:1})):d("",!0)]),_:1},8,["is-window","can-background-cancel"])],64)}const fe=S(Q,[["render",ie]]);export{fe as default};
