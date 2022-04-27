import { useState } from 'react';
import { Text, View, TextInput, Button} from 'react-native';
import React from 'react';
import { StatusBar } from 'expo-status-bar';




const Login = ({navigation} : any) => {
    const[user, setUser] = useState("");
    const[password, setPassword] = useState("");
    const[mensajeDeError, setMensajeDeError] = useState("");

    // ESTRICTAMENTE TEMPORAL
    var global_user = "";
    var global_password = "";

    const login = async() => {
        
        const formData = new FormData();
        formData.append('email', user);
        formData.append('pass', password);
    
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
        }
  };
  const protegido = async () => {

    var headers = new Headers();
    // Authorization Basic

    headers.append("Authorization", global_user + ":" + global_password);
    var response = await fetch('http://127.0.0.1:5000/protegido', {headers: headers});
    alert(await response.text() + " --- " + response.status);
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