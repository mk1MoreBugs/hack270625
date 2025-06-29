import React from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import {
  Image,
  ScrollView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

import { Redirect, router } from "expo-router";
import { useGlobalContext } from "@/lib/global-provider";
import images from "@/constants/images";

const Auth = () => {
  const { login, loading, isLogged } = useGlobalContext();

  if (!loading && isLogged) return <Redirect href="/" />;

  const handleLogin = () => {
    login();
    router.replace("/");
  };

  return (
    <SafeAreaView className="bg-white h-full">
      <ScrollView
        contentContainerStyle={{
          height: "100%",
        }}
      >
        <Image
          source={images.onboarding}
          className="w-full h-4/6"
          resizeMode="contain"
        />

        <View className="px-10">
          <Text className="text-base text-center uppercase font-rubik text-black-200">
            Добро пожаловать в
          </Text>

          <Text className="text-3xl font-rubik-bold text-black-300 text-center mt-2">
            Приложение {"\n"}
            <Text className="text-primary-300">Недвижимости</Text>
          </Text>

          <Text className="text-lg font-rubik text-black-200 text-center mt-12">
            Найдите свой идеальный дом
          </Text>

          <TouchableOpacity
            onPress={handleLogin}
            className="bg-primary-300 rounded-full w-full py-4 mt-5"
          >
            <Text className="text-lg font-rubik-medium text-white text-center">
              Войти в приложение
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Auth;
