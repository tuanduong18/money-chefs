import React, { useState, useContext } from "react";
import { Text, View, TextInput, Button, Alert } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useRouter } from 'expo-router';
import { API_BASE } from "@/constants/api";
import { createStyles } from "./style";
import { Inter_500Medium, useFonts } from "@expo-google-fonts/inter";
import { ThemeContext } from "@/context/ThemeContext";

export default function SignUpScreen() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter()
  const {colorScheme, setColorScheme, theme} = useContext(ThemeContext)
  const [loaded, error] = useFonts({
        Inter_500Medium,
  })

  if (!loaded && !error) {
        return null
  }

  const styles = createStyles(theme, colorScheme)

  const handleSignIn = async () => {

    try {
        const res = await fetch(`${API_BASE}/auth/sign_in`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username,
                password,
            }),
        });
        const data = await res.json()
        if (res.ok) {
        Alert.alert("Success", data.message);
        router.push("/(tabs)/home_screen"); // or any screen you want
        } else {
        Alert.alert("Error", data.message || "Signin failed.");
        }
        
    } catch (error) {
        console.error("Signin error:", error.message);
        Alert.alert("Network Error", error.message);
    }
  };

  return (
    <SafeAreaView style ={{ flex: 1 }}>
      <View style={{ padding: 20 }}>
        <TextInput
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
          style={styles.inputContainer}
        />
        <TextInput
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          style={styles.inputContainer}
        />
        <Button 
          title="Sign In" 
          onPress={handleSignIn} 
          style = {styles.saveButton}
        />
      </View>
    </SafeAreaView>
  );
}