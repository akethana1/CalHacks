import logo from './logo.svg'
import './App.css'
import React, { useState } from 'react'
import axios from 'axios'
import { useReactMediaRecorder  } from "react-media-recorder";
import { AudioRecorder } from 'react-audio-voice-recorder';
import { Circles } from 'react-loader-spinner'

function BackUp() {

  const [text, setText] = useState("")
  const [responseFromAI, setResponseFromAI] = useState("")
  const [theAudio, setTheAudio] = useState(null)
  const [loading, setLoading] = useState(false)
  const [resEmotions, setResEmotions] = useState([])
  const [counter, setCounter] = useState(0)
  const [showSend, setShowSend] = useState(false)

  //the Chat Log
  const [chatLog, setChatLog] = useState([{ role: "assistant", content: "Tell us about a scenario that you want to practice, For example: I want to simulate ordering in a restraurant" }])
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
    setShowSend(false)
    setLoading(true)
    const formData = new FormData();
    formData.append('file', theAudio, 'audio.mp3');
    formData.append('counter', counter + 1);
    formData.append('history', JSON.stringify(chatLog))

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
        { role: "user", content: userText },
        { role: "assistant", content: aiResponse }
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
    setShowSend(true)
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

      <h2 className='instructions'>Press the recording button to talk about what you need help with. Press the green button to
      send your input to the bot.
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
        {
          showSend ? 
          <button className='speak-button' onClick={handeSubmitAudio}>Speak to the AI</button> :
          <></>

        }
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

<div className='Original'>
<h2 className='introAI'>The AI: </h2>
<h2 className='introHuman'>You:</h2>

</div>
<div className="chat-container">
  {chatLog.map((message, index) => (
    <div
      key={index}
      className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
    >
      {message.content}
    </div>
  ))}
</div>
    </div>
  );
}

export default BackUp;
