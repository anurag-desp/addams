/* Copyright 2013 Chris Wilson

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

window.AudioContext = window.AudioContext || window.webkitAudioContext;

var audioContext = new AudioContext();
var audioInput = null,
    realAudioInput = null,
    inputPoint = null,
    audioRecorder = null;
var rafID = null;
var analyserContext = null;
var canvasWidth, canvasHeight;
var recIndex = 0;


function gotBuffers(buffers) {
    audioRecorder.exportMonoWAV(doneEncoding);
}


function doneEncoding(soundBlob) {
    // fetch('/audio', {method: "POST", body: soundBlob}).then(response => $('#output').text(response.text()))
    const loadingShit = document.getElementsByClassName('boxContainer')[0];
    loadingShit.style.display = 'flex';
    console.log(loadingShit)

    fetch('/audio', {method: "POST", body: soundBlob}).then(response => response.json().then(textSentiment => {
        loadingShit.style.display = 'none';
        texts = textSentiment['text'];
        sentiments = textSentiment['sentiments'];
        // sentimentSummary = textSentiment['summary_sentiment'];

        const analysisResult = document.getElementById('analysis-result')
        analysisResult.innerHTML = '<tr>\
                                    <th style="padding: 3px;">Transcription</th>\
                                    <th style="padding: 3px;">Sentiment</th>\
                                    <th style="padding: 3px;">Confidence Score</th>\
                                    </tr>';

        analysisResult.style.display = 'block'; 
        analysisResult.style.padding = '3px'; 
        for (let i = 0; i < texts.length; i++) {
            const tableRow = analysisResult.insertRow(i+1);
            const text = tableRow.insertCell(0);
            const sentiment = tableRow.insertCell(1);
            const score = tableRow.insertCell(2);

            text.innerText = texts[i];
            text.style.padding = '3px';
            sentiment.innerText = sentiments[i][0];
            sentiment.style.padding = '3px';
            sentiment.style.fontWeight = 'bold';
            sentiment.style.color = '#FFFFF2';
            
            score.innerText = (sentiments[i][1].toFixed(5))*100;
            console.log(score.innerText)
            console.log(sentiment)
            score.style.padding = '3px';
            score.style.fontWeight = 'bold';
            score.style.color = '#F5F2B8';
        }

    }));
    var img = document.createElement("img");
    img.src = "{{ url_for('static', filename='img/sns_pie_chart.svg') }}";
    var src = document.getElementById("pie-chart");
    src.appendChild(img);
    recIndex++;
}

function stopRecording() {
    // stop recording
    audioRecorder.stop();
    let startButton = document.getElementById('start');
    document.getElementById('stop').disabled = true;
    startButton.removeAttribute('disabled'); 
    startButton.style.backgroundColor = "#058E3F";
    startButton.innerHTML = "Start Recording";
    audioRecorder.getBuffers(gotBuffers);
}

function startRecording() {

    // start recording
    if (!audioRecorder)
        return;
    let startButton = document.getElementById('start')
    startButton.disabled = true;
    startButton.innerHTML = "Recording...";
    startButton.style.backgroundColor = "#45CB85"
    document.getElementById('stop').removeAttribute('disabled');
    audioRecorder.clear();
    audioRecorder.record();
}

function convertToMono(input) {
    var splitter = audioContext.createChannelSplitter(2);
    var merger = audioContext.createChannelMerger(2);

    input.connect(splitter);
    splitter.connect(merger, 0, 0);
    splitter.connect(merger, 0, 1);
    return merger;
}

function cancelAnalyserUpdates() {
    window.cancelAnimationFrame(rafID);
    rafID = null;
}

function updateAnalysers(time) {
    if (!analyserContext) {
        var canvas = document.getElementById("analyser");
        canvasWidth = canvas.width;
        canvasHeight = canvas.height;
        analyserContext = canvas.getContext('2d');
    }

    // analyzer draw code here
    {
        var SPACING = 3;
        var BAR_WIDTH = 1;
        var numBars = Math.round(canvasWidth / SPACING);
        var freqByteData = new Uint8Array(analyserNode.frequencyBinCount);

        analyserNode.getByteFrequencyData(freqByteData);

        analyserContext.clearRect(0, 0, canvasWidth, canvasHeight);
        analyserContext.fillStyle = '#F6D565';
        analyserContext.lineCap = 'round';
        var multiplier = analyserNode.frequencyBinCount / numBars;

        // Draw rectangle for each frequency bin.
        for (var i = 0; i < numBars; ++i) {
            var magnitude = 0;
            var offset = Math.floor(i * multiplier);
            // gotta sum/average the block, or we miss narrow-bandwidth spikes
            for (var j = 0; j < multiplier; j++)
                magnitude += freqByteData[offset + j];
            magnitude = magnitude / multiplier;
            var magnitude2 = freqByteData[i * multiplier];
            analyserContext.fillStyle = "hsl( " + Math.round((i * 360) / numBars) + ", 100%, 50%)";
            analyserContext.fillRect(i * SPACING, canvasHeight, BAR_WIDTH, -magnitude);
        }
    }

    rafID = window.requestAnimationFrame(updateAnalysers);
}

function toggleMono() {
    if (audioInput != realAudioInput) {
        audioInput.disconnect();
        realAudioInput.disconnect();
        audioInput = realAudioInput;
    } else {
        realAudioInput.disconnect();
        audioInput = convertToMono(realAudioInput);
    }

    audioInput.connect(inputPoint);
}

function gotStream(stream) {
    document.getElementById('start').removeAttribute('disabled');

    inputPoint = audioContext.createGain();

    // Create an AudioNode from the stream.
    realAudioInput = audioContext.createMediaStreamSource(stream);
    audioInput = realAudioInput;
    audioInput.connect(inputPoint);

//    audioInput = convertToMono( input );

    analyserNode = audioContext.createAnalyser();
    analyserNode.fftSize = 2048;
    inputPoint.connect(analyserNode);

    audioRecorder = new Recorder(inputPoint);

    zeroGain = audioContext.createGain();
    zeroGain.gain.value = 0.0;
    inputPoint.connect(zeroGain);
    zeroGain.connect(audioContext.destination);
    updateAnalysers();
}

function initAudio() {
    if (!navigator.getUserMedia)
        navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    if (!navigator.cancelAnimationFrame)
        navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame || navigator.mozCancelAnimationFrame;
    if (!navigator.requestAnimationFrame)
        navigator.requestAnimationFrame = navigator.webkitRequestAnimationFrame || navigator.mozRequestAnimationFrame;

    navigator.getUserMedia(
        {
            "audio": {
                "mandatory": {
                    "googEchoCancellation": "false",
                    "googAutoGainControl": "false",
                    "googNoiseSuppression": "false",
                    "googHighpassFilter": "false"
                },
                "optional": []
            },
        }, gotStream, function (e) {
            alert('Error getting audio');
            console.log(e);
        });
}

window.addEventListener('load', initAudio);

function unpause() {
    document.getElementById('init').style.display = 'none';
    audioContext.resume().then(() => {
        console.log('Playback resumed successfully');
    });
}