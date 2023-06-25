import { configureStore, ThunkAction, Action, combineReducers,  } from '@reduxjs/toolkit';
import settings from '@/features/settings/settingsSlice'
import graph from '@/features/graph/graphSlice';

const reducer = combineReducers({
  settings,
  graph
})

export const store = configureStore({
  reducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
