import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { getAISuggestions } from '@/lib/ai-service';
import type { Property } from '@/lib/types';
import { Card } from './Cards';
import { router } from 'expo-router';

const AIAssistant = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<Property[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) {
      Alert.alert('Ошибка', 'Пожалуйста, введите ваш запрос');
      return;
    }

    setLoading(true);
    try {
      const results = await getAISuggestions(query);
      setSuggestions(results);
      setHasSearched(true);
    } catch (error: any) {
      Alert.alert('Ошибка', error.message || 'Не удалось получить рекомендации');
      console.error('AI suggestions error:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderSuggestion = ({ item }: { item: Property }) => (
    <Card 
      item={item} 
      onPress={() => {
        router.push(`/properties/${item.$id}`);
      }}
    />
  );

  const exampleQueries = [
    "Двухкомнатная квартира в Краснодаре до 6 млн ₽",
    "Студия в Сочи рядом с морем",
    "Трехкомнатная квартира в новостройке СПб",
    "Элитное жилье в Москве с паркингом"
  ];

  const handleExamplePress = (example: string) => {
    setQuery(example);
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        className="flex-1"
      >
        <View className="px-5 pt-5">
          <Text className="text-2xl font-rubik-bold text-black-300 mb-2">
            ИИ-Помощник
          </Text>
          <Text className="text-base font-rubik text-black-200 mb-5">
            Опишите, какую недвижимость вы ищете, и ИИ подберет лучшие варианты
          </Text>

          <View className="mb-5">
            <Text className="text-sm font-rubik-medium text-black-300 mb-2">
              Примеры запросов:
            </Text>
            <View className="flex-row flex-wrap gap-2">
              {exampleQueries.map((example, index) => (
                <TouchableOpacity
                  key={index}
                  onPress={() => handleExamplePress(example)}
                  className="bg-primary-100 px-3 py-2 rounded-full"
                >
                  <Text className="text-xs font-rubik text-primary-300">
                    {example}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          <View className="flex-row gap-3 mb-5">
            <TextInput
              value={query}
              onChangeText={setQuery}
              placeholder="Например: 'Двухкомнатная квартира в Краснодаре до 6 млн ₽'"
              multiline
              className="flex-1 border border-primary-200 rounded-xl px-4 py-3 font-rubik text-black-300 min-h-[100px]"
              textAlignVertical="top"
            />
          </View>

          <TouchableOpacity
            onPress={handleSearch}
            disabled={loading}
            className={`bg-primary-300 rounded-xl py-4 mb-5 ${loading ? 'opacity-50' : ''}`}
          >
            {loading ? (
              <View className="flex-row items-center justify-center">
                <ActivityIndicator color="white" size="small" />
                <Text className="text-white text-center font-rubik-medium text-lg ml-2">
                  ИИ анализирует запрос...
                </Text>
              </View>
            ) : (
              <Text className="text-white text-center font-rubik-medium text-lg">
                🤖 Получить рекомендации ИИ
              </Text>
            )}
          </TouchableOpacity>
        </View>

        {hasSearched && (
          <View className="flex-1 px-5">
            <Text className="text-xl font-rubik-bold text-black-300 mb-4">
              Рекомендации ИИ ({suggestions.length})
            </Text>

            {suggestions.length === 0 ? (
              <View className="flex-1 justify-center items-center">
                <Text className="text-lg font-rubik text-black-200 text-center">
                  ИИ не смог найти подходящие варианты.{'\n'}
                  Попробуйте изменить критерии поиска или{'\n'}
                  воспользуйтесь примерами запросов выше.
                </Text>
              </View>
            ) : (
              <FlatList
                data={suggestions}
                renderItem={renderSuggestion}
                keyExtractor={(item) => item.$id}
                numColumns={2}
                columnWrapperStyle={{ gap: 16 }}
                contentContainerStyle={{ gap: 16, paddingBottom: 100 }}
                showsVerticalScrollIndicator={false}
              />
            )}
          </View>
        )}

        {!hasSearched && (
          <View className="flex-1 justify-center items-center px-5">
            <Text className="text-lg font-rubik text-black-200 text-center mb-4">
              🤖 Искусственный интеллект поможет найти{'\n'}
              идеальную недвижимость под ваши запросы
            </Text>
            <Text className="text-sm font-rubik text-black-100 text-center">
              Просто опишите что вы ищете, и ИИ{'\n'}
              сгенерирует персональные рекомендации
            </Text>
          </View>
        )}
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default AIAssistant; 