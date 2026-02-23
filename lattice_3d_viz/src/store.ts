import { create } from 'zustand';

interface TimeState {
    currentDay: number;
    isPlaying: boolean;
    setDay: (day: number) => void;
    togglePlay: () => void;
}

export const useTimeStore = create<TimeState>((set) => ({
    currentDay: 0,
    isPlaying: true,
    setDay: (day: number) => set({ currentDay: day }),
    togglePlay: () => set((state) => ({ isPlaying: !state.isPlaying })),
}));
