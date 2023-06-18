import logo from './logo.svg'
import './App.css'
import React, { useState } from 'react'
import axios from 'axios'
import { useReactMediaRecorder  } from "react-media-recorder";
import { AudioRecorder } from 'react-audio-voice-recorder';

function Temp() {

  const [text, setText] = useState("")
  const [responseFromAI, setResponseFromAI] = useState("")
  const [theAudio, setTheAudio] = useState(null)
  const {
    status,
    startRecording,
    stopRecording,
    mediaBlobUrl,
  } = useReactMediaRecorder({ audio: true })


  const handleStopRecording = async () => {

    await stopRecording()
    console.log(mediaBlobUrl)
    console.log("hello")

    const formData = new FormData()
    // formData.append('audio', mediaBlobUrl, 'recorded_audio.webm');
    // formData.append('format', 'mp3');


  }
  const handleSubmit = () => {
    const data = {
      "text": text
    }
    axios.post("http://127.0.0.1:8000/testing/", data)
      .then((res) => {
        setResponseFromAI(res.data.choices[0]["text"])
      })
  }


  const handeSubmitAudio = () => {
    
  }

  const convertBlobToBase64 = (blob, callback) => {
    const reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = () => {
      const base64String = reader.result.split(',')[1];
      callback(base64String);
    };
  }

  const addAudioElement = (blob) => {
    setTheAudio(blob)
    convertBlobToBase64(blob, (base64String) => {
      console.log(base64String);
    });

    const url = URL.createObjectURL(blob)
    console.log(url)
    // const audio = document.createElement("audio");
    // audio.src = url
    // audio.controls = true
    // document.body.appendChild(audio);
  }
  return (
    <div className="App">
      <h1>Learn English</h1>
      <input
        type="text"
        value={text}
        onChange={event => setText(event.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button>
      <button onClick={handeSubmitAudio}>Submit Audio</button>
      <div>
        {responseFromAI}
      </div>

      <AudioRecorder 
      onRecordingComplete={addAudioElement}
      audioTrackConstraints={{
        noiseSuppression: true,
        echoCancellation: true,
      }} 
      downloadOnSavePress={false}
      downloadFileExtension="mp3"
    />
    </div>
  );
}

export default Temp;
