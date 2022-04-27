import { useState } from 'react';
import { Text, View, FlatList } from 'react-native';
import React from 'react';
import Item from '../Components/Item';
import { StatusBar } from 'expo-status-bar';
import  { useEffect } from "react";


const Principal = ({navigation} : any) => {

    const useMountEffect = (fun: any) => useEffect(fun, []);

    const[cargando, setCargando] = useState(true);
    const[datos, setDatos] = useState([]);
    const navigationAction =(nombre : any,peso: any,id: any) => {
      console.log("ayuda");
      navigation.navigate("Detalle", {nombre: nombre, peso: peso, id: id});
    }
   
  
    const solicitud = async() => {
  
      //var respuesta = await fetch("https://raw.githubusercontent.com/gmorivastec/TC3005B_FRONTEND_APR4/master/gatitos.json");
      var respuesta = await fetch("http://127.0.0.1:5000/");
      setDatos(await respuesta.json());
      setCargando(false);
    };
    useMountEffect(solicitud);
  
    return (
      <View>
        <Text> ITEMS </Text>
  
        {cargando && <Text>CARGANDO...</Text>}
        {datos && (
          <FlatList 
            data={datos}
            renderItem={({item}: any) =>
              <Item
                nombre={item.nombre}
                peso={item.peso}
                id={item.id}
                action = {navigationAction}
              />
            }
          />
        )}
  
        
        <StatusBar style="auto" />
      </View>
    );
  }
  export default Principal;