import {Text, View } from 'react-native';
import React from 'react';

const Detalle = ({route} : any) => {

    return (
      <View >
        <Text> {route.params.nombre} </Text>
        <Text> --------------------------------------------- </Text>
        <Text> PESO: {route.params.peso} </Text>
        <Text> ID: {route.params.id} </Text>
      </View>
    );
  }
  export default Detalle;