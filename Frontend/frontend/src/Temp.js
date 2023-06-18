import logo from './logo.svg'
import './App.css'
import React, { useState } from 'react'
import axios from 'axios'
import { useReactMediaRecorder  } from "react-media-recorder";
import { AudioRecorder } from 'react-audio-voice-recorder';
import { Circles } from 'react-loader-spinner'

function Temp() {

  const [text, setText] = useState("")
  const [responseFromAI, setResponseFromAI] = useState("")
  const [theAudio, setTheAudio] = useState(null)
  const [loading, setLoading] = useState(false)
  const [resEmotions, setResEmotions] = useState([])
  const [counter, setCounter] = useState(0)

  //the Chat Log
  const [chatLog, setChatLog] = useState([{ type: "user", message: "userText" }])
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
    setLoading(true)
    const formData = new FormData();
    formData.append('file', theAudio, 'audio.mp3');
    formData.append('counter', counter + 1);

    axios.post('http://127.0.0.1:8000/audioUpload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
      // Handle the response from the server
      console.log('Upload successful:', response.data);
      setLoading(false)
      setResEmotions([response.data["aiResponse"]])

      const userText = response.data["userText"]
      const aiResponse = response.data["aiResponse"]
      setChatLog(prevChat => [
        ...prevChat,
        { type: "user", message: userText },
        { type: "ai", message: aiResponse }
      ])
      setCounter(counter + 1)
      console.log(chatLog)
    })
    .catch(error => {
      // Handle any error that occurred during the upload
      console.error('Error uploading file:', error);
    })
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
    <div className='App'>
      <h1>AILoveEnglish!</h1>
      <h2>Instructions: Record the phrase you want scrutinized by pressing the recording button 
        on the left. Next, tell us under what context the phrase occurs in.
      </h2>
      {/* <input
        type="text"
        value={text}
        onChange={event => setText(event.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button> */}
      <div>
        {responseFromAI}
      </div>

      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <AudioRecorder
          onRecordingComplete={addAudioElement}
          audioTrackConstraints={{
            noiseSuppression: true,
            echoCancellation: true,
          }}
          downloadOnSavePress={false}
          downloadFileExtension="wav"
        />
              <button onClick={handeSubmitAudio}>Speak to the AI</button>
              <br></br>
              <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              {
        loading ? (
          <Circles
            height="80"
            width="80"
            radius="9"
            color="green"
            ariaLabel="circles-loading"
            wrapperStyle={{ display: 'block' }} // Set display to 'block'
            wrapperClass={null}



          />
        ) : (
          <></>
        )
      }
              </div>


      </div>



<div className="chat-container">
  {chatLog.map((message, index) => (
    <div
      key={index}
      className={`message ${message.type === 'user' ? 'user-message' : 'ai-message'}`}
    >
      {message.message}
    </div>
  ))}
</div>
    </div>
  );
}

export default Temp;
