import{d as g,A as d,g as u,_ as p,r as l,o as D,c as f,h as r,t as n,e as t}from"./index-32431f85.js";import{I as T}from"./Dropable_Image01-0ca12740.js";import{f as V}from"./form-dropdown01-df27a954.js";import{t as h}from"./textbox-form01number-78974892.js";import{s as E}from"./slider-form01-84532fd0.js";const I=g({setup(){},components:{Img_Comp01:T,"text-form-number":h,"slider-form":E,"select-form":V},async created(){this.ImageEditData=d().getImageEditSetting;const e=await this.axios.post(u()+"/api/processing-images/get-trimming-models");this.trimmingModels=e.data.models},unmounted(){d().setImageEditSetting(this.ImageEditData)},watch:{ImageEditData:{handler(e,a){d().setImageEditSetting(e)},deep:!0}},data(){return{ImageEditData:{},rembgModels:["u2net","u2netp","u2net_human_seg","u2net_cloth_seg","silueta","isnet-general-use","isnet-anime","sam"],trimmingModels:[],resizeModels:["RealESRGAN_x4plus","RealESRNet_x4plus","RealESRGAN_x4plus_anime_6B","RealESRGAN_x2plus"]}},methods:{changeModel(e){},updateSliderValue(){this.$nextTick(()=>{this.$forceUpdate()})}}}),_={class:"flex flex-col text-white font-Raleway border-winBorder border-white rounded-lg p-3 overflow-y-auto max-h-[600px]"},C={class:"text-xl"},$={class:"grid grid-cols-3 gap-4 my-4 ml-6"},y={class:"text-xl"},U={class:"grid grid-cols-3 gap-2 my-4 ml-6"},B={class:"text-xl"},b={class:"grid grid-cols-3 gap-4 my-4 ml-6"},R={class:"text-xl"},S={class:"grid grid-cols-3 gap-4 my-4 ml-6"};function z(e,a,F,M,N,w){const o=l("select-form"),s=l("text-form-number"),i=l("slider-form");return D(),f("div",_,[r("p",C,n(e.$t("CharacterTrimming.setting.CharactersTrimming")),1),r("div",$,[t(o,{choices:e.rembgModels,"form-name":e.$t("CharacterTrimming.setting.ModelName"),modelValue:e.ImageEditData.Character_Trimming_Data.modelname,"onUpdate:modelValue":a[0]||(a[0]=m=>e.ImageEditData.Character_Trimming_Data.modelname=m)},null,8,["choices","form-name","modelValue"]),t(s,{"form-name":e.$t("CharacterTrimming.setting.spread"),modelValue:e.ImageEditData.Character_Trimming_Data.spread,"onUpdate:modelValue":a[1]||(a[1]=m=>e.ImageEditData.Character_Trimming_Data.spread=m)},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.erode_size"),modelValue:e.ImageEditData.Character_Trimming_Data.erode_size,"onUpdate:modelValue":a[2]||(a[2]=m=>e.ImageEditData.Character_Trimming_Data.erode_size=m),min:1,max:50,step:1},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.foreground_threshold"),modelValue:e.ImageEditData.Character_Trimming_Data.foreground_threshold,"onUpdate:modelValue":a[3]||(a[3]=m=>e.ImageEditData.Character_Trimming_Data.foreground_threshold=m),min:0,max:255,step:1},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.background_threshold"),modelValue:e.ImageEditData.Character_Trimming_Data.background_threshold,"onUpdate:modelValue":a[4]||(a[4]=m=>e.ImageEditData.Character_Trimming_Data.background_threshold=m),min:0,max:255,step:1},null,8,["form-name","modelValue"])]),r("p",y,n(e.$t("CharacterTrimming.setting.FaceTrimming")),1),r("div",U,[t(o,{choices:e.trimmingModels,"form-name":e.$t("CharacterTrimming.setting.ModelName"),modelValue:e.ImageEditData.Face_Trimming_Data.modelname,"onUpdate:modelValue":a[5]||(a[5]=m=>e.ImageEditData.Face_Trimming_Data.modelname=m)},null,8,["choices","form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.spread_top"),modelValue:e.ImageEditData.Face_Trimming_Data.spread_top,"onUpdate:modelValue":a[6]||(a[6]=m=>e.ImageEditData.Face_Trimming_Data.spread_top=m),min:.05,max:4,step:.01},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.spread_left"),modelValue:e.ImageEditData.Face_Trimming_Data.spread_left,"onUpdate:modelValue":a[7]||(a[7]=m=>e.ImageEditData.Face_Trimming_Data.spread_left=m),min:.05,max:4,step:.01},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.spread_right"),modelValue:e.ImageEditData.Face_Trimming_Data.spread_right,"onUpdate:modelValue":a[8]||(a[8]=m=>e.ImageEditData.Face_Trimming_Data.spread_right=m),min:.05,max:4,step:.01},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.spread_bottom"),modelValue:e.ImageEditData.Face_Trimming_Data.spread_bottom,"onUpdate:modelValue":a[9]||(a[9]=m=>e.ImageEditData.Face_Trimming_Data.spread_bottom=m),min:.05,max:4,step:.01},null,8,["form-name","modelValue"])]),r("p",B,n(e.$t("CharacterTrimming.setting.BodyTrimming")),1),r("div",b,[t(o,{choices:e.trimmingModels,"form-name":e.$t("CharacterTrimming.setting.ModelName"),modelValue:e.ImageEditData.Body_Trimming_Data.modelname,"onUpdate:modelValue":a[10]||(a[10]=m=>e.ImageEditData.Body_Trimming_Data.modelname=m)},null,8,["choices","form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.spread_top"),modelValue:e.ImageEditData.Body_Trimming_Data.spread_top,"onUpdate:modelValue":a[11]||(a[11]=m=>e.ImageEditData.Body_Trimming_Data.spread_top=m),min:.05,max:4,step:.01},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.spread_left"),modelValue:e.ImageEditData.Body_Trimming_Data.spread_left,"onUpdate:modelValue":a[12]||(a[12]=m=>e.ImageEditData.Body_Trimming_Data.spread_left=m),min:.05,max:4,step:.01},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.spread_right"),modelValue:e.ImageEditData.Body_Trimming_Data.spread_right,"onUpdate:modelValue":a[13]||(a[13]=m=>e.ImageEditData.Body_Trimming_Data.spread_right=m),min:.05,max:4,step:.01},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.spread_bottom"),modelValue:e.ImageEditData.Body_Trimming_Data.spread_bottom,"onUpdate:modelValue":a[14]||(a[14]=m=>e.ImageEditData.Body_Trimming_Data.spread_bottom=m),min:.05,max:4,step:.01},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.width_rate"),modelValue:e.ImageEditData.Body_Trimming_Data.width_rate,"onUpdate:modelValue":a[15]||(a[15]=m=>e.ImageEditData.Body_Trimming_Data.width_rate=m),min:.05,max:4,step:.01},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.height_rate"),modelValue:e.ImageEditData.Body_Trimming_Data.height_rate,"onUpdate:modelValue":a[16]||(a[16]=m=>e.ImageEditData.Body_Trimming_Data.height_rate=m),min:.05,max:4,step:.01},null,8,["form-name","modelValue"])]),r("p",R,n(e.$t("CharacterTrimming.setting.Resize")),1),r("div",S,[t(s,{"form-name":e.$t("CharacterTrimming.setting.SideLength"),modelValue:e.ImageEditData.Resize.lengthSide,"onUpdate:modelValue":a[17]||(a[17]=m=>e.ImageEditData.Resize.lengthSide=m)},null,8,["form-name","modelValue"]),t(i,{"form-name":e.$t("CharacterTrimming.setting.RateLimitation"),modelValue:e.ImageEditData.Resize.rateLimitation,"onUpdate:modelValue":a[18]||(a[18]=m=>e.ImageEditData.Resize.rateLimitation=m),min:1,max:4,step:1},null,8,["form-name","modelValue"]),t(o,{choices:e.resizeModels,"form-name":e.$t("CharacterTrimming.setting.resizeModel"),modelValue:e.ImageEditData.Resize.modelName,"onUpdate:modelValue":a[19]||(a[19]=m=>e.ImageEditData.Resize.modelName=m)},null,8,["choices","form-name","modelValue"])])])}const j=p(I,[["render",z]]);export{j as default};
