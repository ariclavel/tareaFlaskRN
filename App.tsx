import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Principal from "./Components/Principal";
import Detalle from "./Components/Detalle";



function App() {
  const Stack = createNativeStackNavigator();
  
  return (
    <div className="App">
      <NavigationContainer linking={{enabled: true}}>
      <Stack.Navigator screenOptions={{headerShown: false}}>
        <Stack.Screen 
          name="Principal"
          component={Principal}
        />
        <Stack.Screen 
          name="Detalle"
          component={Detalle}
        />
      </Stack.Navigator>
    </NavigationContainer>
    </div>
  );
  
}

export default App;


