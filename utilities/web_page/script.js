let sost = 'False'
let sost2 = 'False'
let sost3 = 'False'
let sost4 = 'False'

document.getElementById("zag_habr").onclick = function(event) { 
    
    if (sost == 'False')
    {
        document.getElementById("ul_habr").style = 'display: block'
        sost = 'True'
    }
    else
    {
        document.getElementById("ul_habr").style = 'display: none'
        sost = 'False'       
    }
    
};

document.getElementById("zag_itprog").onclick = function(event) { 
    
    if (sost2 == 'False')
    {
        document.getElementById("ul_itprog").style = 'display: block'
        sost2 = 'True'
    }
    else
    {
        document.getElementById("ul_itprog").style = 'display: none'
        sost2 = 'False'       
    }
    
};

document.getElementById("zag_another").onclick = function(event) { 
    
    if (sost3 == 'False')
    {
        document.getElementById("ul_another").style = 'display: block'
        sost3 = 'True'
    }
    else
    {
        document.getElementById("ul_another").style = 'display: none'
        sost3 = 'False'       
    }
    
};

document.getElementById("zag_sof").onclick = function(event) { 
    
    if (sost4 == 'False')
    {
        document.getElementById("ul_sof").style = 'display: block'
        sost4 = 'True'
    }
    else
    {
        document.getElementById("ul_sof").style = 'display: none'
        sost4 = 'False'       
    }
    
};