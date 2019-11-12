%script for quick formating of charts

color_flg = 1;

if(color_flg)
    set(groot,'defaultAxesColorOrder',...
        [ 0  ,50 ,135; 200,20 ,30 ; 0  ,120,0  ; 120,90 ,0  ;...
            150,50 ,165; 10 ,145,120; 0  ,0  ,0  ; 220,150,20 ;...
            200,150,200; 255,255,0  ; 255,0  ,128; 150,150,0  ;...
            0  ,255,255; 0  ,255,0  ; 255,80  ,255]/255);
else
    set(groot,'defaultAxesColorOrder',[0,0,0]); %only 1 color so we loop linestyle
end
set(groot,'defaultFigureUnits','Inches');
set(groot,'defaultFigurePosition',[2,2,5,4]);
set(groot,'defaultAxesLineStyleOrder','-|--|:|-.|-+|--o|:*|-..|-x|--s|:d|-.^|-v|-->|:p');
%set(groot,'defaultAxesFontSize',12);
set(groot,'defaultAxesFontSize',24);
set(groot,'DefaultAxesTitleFontSizeMultiplier', 1);
set(0,'DefaultLineLineWidth',2);
set(0,'DefaultTextFontSize',24);