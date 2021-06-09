var tiles = document.getElementById('tilesId');
var setNum = document.getElementById('setNum');
var question1 = document.getElementById('q1');
var question2 = document.getElementById('q2');
var set = document.getElementById('loadSet');
var question1ToDisplay, question2ToDisplay;
var data = [];
var numOfQuestions = 2
var ordNum = 1;
var numberOfSets = 0;
var logs = [];


var cancel = document.getElementById('cancel').addEventListener('click', () => {
    setNum.innerHTML = 'Set Number';
    question1.innerHTML = 'Question 1';
    question2.innerHTML = 'Question 2';
});

var downloadLogs = document.getElementById('downloadLogs').addEventListener('click', () => downloadCSV(logs));

set.onchange = function () {
    loadFile(data, set);
}

function addTiles() {
    for (var n = 1; n < numberOfSets + 1; n++) {
        var div = document.createElement('tile');
        div.id = n;
        div.className = 'tile';
        div.innerHTML = n;
        div.addEventListener('click', e => {
            e.target.style.backgroundColor = '#BBBBBB';
            setChosen = data[e.target.id * (numOfQuestions + 1) - 3];
            question1ToDisplay = data[e.target.id * (numOfQuestions + 1) - 2];
            question2ToDisplay = data[e.target.id * (numOfQuestions + 1) - 1];
            setNum.innerHTML = setChosen;
            question1.innerHTML = question1ToDisplay;
            question2.innerHTML = question2ToDisplay;
            logs.push(['stundent numer' + ordNum, new Date(Date.now()).toLocaleString(), setChosen, question1ToDisplay, question2ToDisplay]);
            ordNum++;

        })
        tiles.appendChild(div);
    }
}

function loadFile(data, docId) {
    var file = docId.files[0];
    var reader = new FileReader();

    reader.addEventListener('loadend', addTiles);

    reader.onload = function () {
        data.length = 0;
        var content = this.result.split('\n');
        numberOfSets = content.length / (numOfQuestions + 1);
        content.forEach(a => data.push(a.trim()));
    }
    reader.readAsText(file);
}

function downloadCSV(data) {
    console.log(data);
    let csv = "data:text/csv;charset=utf-8," + data.map(line => line.join(";")).join("\n");
    var uriEncoded = encodeURI(csv);
    var link = document.createElement("a");
    link.setAttribute("href", uriEncoded);
    link.setAttribute("download", "domande.csv");
    document.body.appendChild(link);
    link.click();
}
