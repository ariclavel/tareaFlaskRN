import { useState } from 'react';
import { Text, View, TextInput, Button} from 'react-native';
import React from 'react';
import { StatusBar } from 'expo-status-bar';
import  { useEffect } from "react";


const Login = ({navigation} : any) => {
    
    const[user, setUser] = useState('a@gmail.com');
    const[password, setPassword] = useState("");
    const[token, setToken] = useState("1111");
    const[mensajeDeError, setMensajeDeError] = useState("");

    // ESTRICTAMENTE TEMPORAL
    var global_user = "";
    var global_password = "";
    

    const solicitud = async() => {
      const e = 'a@gmail.com';
      const formData = new FormData();
      formData.append('e', user);
      var respuesta = await fetch('http://127.0.0.1:5000/users', {
          method: 'POST',
          body: formData
        
      });
      //var respuesta = await fetch("http://127.0.0.1:5000/users");
      var a = await respuesta.json();
      console.log(await a[0][2]);
      setUser(a[0][1]);
      setPassword(a[0][2]);
      setPassword(a[0][3]);

    
    };
    const useMountEffect = (fun: any) => useEffect(fun, []);
    useMountEffect(solicitud);
    const login = async() => {
        
        const formData = new FormData();
        formData.append('email', user);
        formData.append('password', password);
        
    
        // solicitud con POST y con datos 
        var response = 
        await fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          body: formData
        
        });

        alert(await response.text() + " ::: " + response.status);
        if(response.status == 200){
            global_user = user;
            global_password = password;
            navigation.navigate("Principal", {token: token});
            
        }
  };
  const protegido = async () => {

    var headers = new Headers();
    // Authorization Basic

    headers.append("Authorization", user + ":" + password);
    var response = await fetch('http://127.0.0.1:5000/protegido', {headers: headers});
    alert(await response.text() + " --- " + response.status);
    if(response.status == 200){
      
      navigation.navigate("Principal", {token: token});
      
    }
  };
   
    return (
      <View>
        <Text>{mensajeDeError}</Text>
        <TextInput 
            placeholder='user'
            onChangeText={text => {
            setUser(text);
            }}
        />
        <TextInput 
            placeholder='password'
            secureTextEntry={true}
            onChangeText={text => {
            setPassword(text);
            }}
        />
        <Button 
            title="LOGIN"
            onPress={() => {
            login();
            }}
        />
        <Button 
            title="PROTEGIDO"
            onPress={() => {
            protegido();
            }}
        /> 
        <StatusBar style="auto" />
      </View>
    );
  }
  export default Login;