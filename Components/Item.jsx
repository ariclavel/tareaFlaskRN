import {Text, View, Button } from 'react-native';
import React from 'react';
const Item = (props) => {
    return(<View>
        <Text> {props.nombre} </Text>
        <Button
          key = {props.id}
          title= "ver detalle"
          onPress={() => {props.action(props.nombre, props.peso, props.id)}}
         >
           Ver detalle
         </Button>
         
      </View>);
  }
  export default Item;