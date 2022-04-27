import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Principal from "./Pages/Principal";
import Detalle from "./Components/Detalle";
import Login from './Pages/Login';



function App() {
  const linking = {
    enabled: true,
    config: {
      screens: {
        Login: '',
        Principal: '/main'
      }
    }
  };
  const Stack = createNativeStackNavigator();
  
  return (
    <div className="App">
      <NavigationContainer linking={{enabled: true}}>
      <Stack.Navigator screenOptions={{headerShown: false}}>
        <Stack.Screen 
          name="Login"
          component={Login}
        />
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


