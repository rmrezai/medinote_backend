import { createContext, useContext, useState, useEffect } from 'react';

const AppStateContext = createContext();

export const AppStateProvider = ({ children }) => {
  const [patientData, setPatientData] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('patientData')) || {};
    } catch {
      return {};
    }
  });

  const [note, setNote] = useState(() => localStorage.getItem('note') || '');

  useEffect(() => {
    try {
      localStorage.setItem('patientData', JSON.stringify(patientData));
    } catch {
      // ignore write errors
    }
  }, [patientData]);

  useEffect(() => {
    try {
      localStorage.setItem('note', note);
    } catch {
      // ignore write errors
    }
  }, [note]);

  return (
    <AppStateContext.Provider value={{ patientData, setPatientData, note, setNote }}>
      {children}
    </AppStateContext.Provider>
  );
};

export const usePatientData = () => {
  const { patientData, setPatientData } = useContext(AppStateContext);
  return [patientData, setPatientData];
};

export const useNote = () => {
  const { note, setNote } = useContext(AppStateContext);
  return [note, setNote];
};

export default AppStateContext;
