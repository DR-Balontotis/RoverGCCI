// global vars
let terminal, writeSpeed;

window.addEventListener('load', init);

function init() {
    // default settings
    terminal = document.getElementById("terminal-promt-result");
    writeSpeed = 120;
    terminalStart();
}

function terminalStart() {
    TerminalWrite_cursor();
}


function terminalWrite(text)
{
    terminal.value = (`${(terminal.value).replace("|","")}${text}`);
    
    /*
    terminal.blur();
    terminal.focus();
    */
}

function TerminalWrite_cursor()
{
    terminalWrite('$> ');
}