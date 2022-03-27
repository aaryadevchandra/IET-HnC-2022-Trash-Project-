import React, { Component } from 'react'
import { GoogleMap, LoadScript } from '@react-google-maps/api';
import 'bootstrap/dist/css/bootstrap.css';
import { Marker } from '@react-google-maps/api';
import logo from "./Assets/logo.png";
import { useState } from 'react';
import axios from 'axios';







const containerStyle = {
  width: '1000px',
  height: '600px'
};

const center = {
  lat: -3.745,
  lng: -38.523
};


// const position = {
//   lat: 37.772,
//   lng: -122.214
// }





function MyComponent() {

  let [results, setResults] = useState([]);

  const onLoad = marker => {
    console.log('marker: ', marker)
  }


  async function getlocs(){
    const response = await axios.post(
        'http://localhost:3004/marker'
        ).catch(err => {
          console.log(err)
        });


        // response.data.map(doc=>console.log(doc.lat))
        setResults(results = response.data.map((document)=>{
          return <Marker onLoad={onLoad} position={{lat: parseFloat(document.lat), lng: parseFloat(document.lng)}} /> 
        }))
}
  getlocs();
  return (
    <div>
  
  
    <nav class="navbar navbar-dark bg-dark" style={{padding:"25px 50px"}}>
      <a class="navbar-brand" href="#">
        <img src={logo} width="80" height="80" alt="Logo"/>
      </a>

      <ul class="navbar-nav">
        <li class="nav-item active">
          <a class="nav-link" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">About Us</a>
        </li>
      </ul>
    </nav>




    <div style={{
      position: 'absolute', left: '50%', top: '50%',
      transform: 'translate(-50%, -50%)',
      paddingTop: '100px'
      }}>

  
    <LoadScript
      googleMapsApiKey="AIzaSyDcCVE991iVGqrHdIhTM6Rl-XmKMXwbYxQ"
    >
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={10}
      >

      {results}
        <></>
      </GoogleMap>
    </LoadScript>
    </div>
    </div>
  )
}

export default React.memo(MyComponent)