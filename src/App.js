import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';


function App() {
  //const [name, setName] = useState([]);
  //const [current, setCurrent] = useState(0);
  //
  //console.log(name)
//
  //useEffect(() => {
  //  fetch('/image_info').then(res => res.json()).then(data => {
  //    setCurrent(data);
  //  });
  //}, []);

  return (
    <div className="App">
      <header className="App-header" >   

      ...Copie y pegue en este recuadro la ruta de la imagen a convertir para el formato de papel A4...
      
      <form action="/image_info" method="post">
        <input type="text" name="email"></input>
        <input type="submit" value="Ruta"></input>
      </form>   
      </header>
    </div>
  );
}

export default App;