import {Text, View, Button, FlatList } from 'react-native';
import React from 'react';
const Item = (props) => {
    return(<View>
        <Text> {props.nombre} </Text>
        <Button
          key = {props.nombre}
          title= "ver detalle"
          onPress={() => {props.action(props.nombre, props.peso, props.edad)}}
         >
           Ver detalle
         </Button>
         
      </View>);
  }
  export default Item;