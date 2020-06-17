function [ roundNum ] = round_arb( input, base )
%@brief Round 'input' to integer multiple of arbitrary 'base'
%@param[in] input - value to round
%@param[in] base - base to round to integer multiple of
%@return Rounded value
    roundNum = base.*round(input./base);
end
