function [pi_str] = num2pi(number)
%@brief Change a decimal number (e.g. 1.56...) to a pi fraction string (e.g. '\pi/2')
%@param[in] number - floating point number to convert
%%%%@param[NA] latex_flg - whether or not to return latex fraction
%@return chararray of pi fraction with \pi for pi
    [n,d] = rat(number/pi); %first get the fraction
    if n==0 %then just return 0
        pi_str = '0';
    else %otherwise build the correct string
        pi_str = sprintf('%d\\pi/%d',n,d);
        pi_str = regexprep(pi_str,'1\\pi','\\pi'); %fix 1\pi
        pi_str = regexprep(pi_str,'/1',''); %fix divided by 1 
    end
    %if latex_flg %change / to frac{}{}
    %    pi_str = ['frac{',regexprep(pi_str,'/','}{'),'}'];
    %end
end

%{
%test
test_val = pi/2
num2pi(test_val)
%}
