import {
  MARITAL_STATUS_OPTIONS,
  GENDER_OPTIONS,
  DAYTIME_EVENING_OPTIONS,
  COURSE_OPTIONS,
  APPLICATION_MODE_OPTIONS,
  QUALIFICATION_OPTIONS,
  OCCUPATION_OPTIONS,
  YES_NO_OPTIONS
} from '../constants/datasetOptions';
import i18n from '../i18n';

export const getOptionLabel = (value: number | undefined, options: { label: string; value: number }[]): string => {
  if (value === undefined) return 'N/A';
  const option = options.find((opt) => opt.value === value);
  return option ? option.label : `Unknown (${value})`;
};

export const getMaritalStatusLabel = (value: number): string => {
  const key = `options.marital.${value}`;
  return i18n.global.te(key) ? i18n.global.t(key) : getOptionLabel(value, MARITAL_STATUS_OPTIONS);
};

export const getGenderLabel = (value: number): string => {
  const key = `options.gender.${value}`;
  return i18n.global.te(key) ? i18n.global.t(key) : getOptionLabel(value, GENDER_OPTIONS);
};

export const getDaytimeEveningLabel = (value: number): string => {
  const key = `options.shift.${value}`;
  return i18n.global.te(key) ? i18n.global.t(key) : getOptionLabel(value, DAYTIME_EVENING_OPTIONS);
};

export const getYesNoLabel = (value: number): string => {
  const key = `options.yesNo.${value}`;
  return i18n.global.te(key) ? i18n.global.t(key) : getOptionLabel(value, YES_NO_OPTIONS);
};

export const getCourseLabel = (value: number): string => {
  const key = `options.course.${value}`;
  return i18n.global.te(key) ? i18n.global.t(key) : getOptionLabel(value, COURSE_OPTIONS);
};

export const getApplicationModeLabel = (value: number): string => {
  const key = `options.applicationMode.${value}`;
  return i18n.global.te(key) ? i18n.global.t(key) : getOptionLabel(value, APPLICATION_MODE_OPTIONS);
};

export const getQualificationLabel = (value: number): string => {
  const key = `options.qualification.${value}`;
  return i18n.global.te(key) ? i18n.global.t(key) : getOptionLabel(value, QUALIFICATION_OPTIONS);
};

export const getOccupationLabel = (value: number): string => {
  const key = `options.occupation.${value}`;
  return i18n.global.te(key) ? i18n.global.t(key) : getOptionLabel(value, OCCUPATION_OPTIONS);
};
