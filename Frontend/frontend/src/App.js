import logo from './logo.svg'
import './App.css'
import React, { useState } from 'react'
import axios from 'axios'
import { AudioRecorder } from 'react-audio-voice-recorder';
import { useReactMediaRecorder  } from "react-media-recorder";
function App() {

  const [text, setText] = useState("")
  const [responseFromAI, setResponseFromAI] = useState("")
  const [recordedAudio, setRecordedAudio] = useState(null)
  // const {
  //   status,
  //   startRecording,
  //   stopRecording,
  //   mediaBlobUrl,
  // } = useReactMediaRecorder({ audio: true })


  const handleStopRecording =  () => {

    console.log("hello")
    // await stopRecording()
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
  return (
    <div className="App">
      <h1>Learn English</h1>
      <input
        type="text"
        value={text}
        onChange={event => setText(event.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button>
      <div>
        {responseFromAI}
      </div>

      <div>

      <button onClick={handleStopRecording}>
        Stop Recording
      </button>
      {/* {mediaBlobUrl && (
        <audio src={mediaBlobUrl} controls autoPlay />
      )} */}
    </div>
    </div>
  );
}

export default App
