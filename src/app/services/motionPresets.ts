export const MOTION_EASE = [0.22, 1, 0.36, 1] as const;
export const STAGGER_DELAY_STEP = 0.03;

export const PAGE_TRANSITION = {
  duration: 0.18,
  ease: MOTION_EASE,
};

export const REDUCED_PAGE_TRANSITION = {
  duration: 0.01,
  ease: "linear" as const,
};

export const PAGE_VARIANTS = {
  hidden: { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 1, y: 0 },
};

export const REDUCED_PAGE_VARIANTS = {
  hidden: { opacity: 1, y: 0 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 1, y: 0 },
};

export const SECTION_MOTION_PRESETS = {
  hero: {
    variants: {
      hidden: { opacity: 0, y: 10 },
      visible: { opacity: 1, y: 0 },
    },
    transition: {
      duration: 0.2,
      ease: MOTION_EASE,
    },
  },
  section: {
    variants: {
      hidden: { opacity: 0, y: 8 },
      visible: { opacity: 1, y: 0 },
    },
    transition: {
      duration: 0.18,
      ease: MOTION_EASE,
    },
  },
  card: {
    variants: {
      hidden: { opacity: 0, y: 6 },
      visible: { opacity: 1, y: 0 },
    },
    transition: {
      duration: 0.16,
      ease: MOTION_EASE,
    },
  },
  form: {
    variants: {
      hidden: { opacity: 0, y: 6 },
      visible: { opacity: 1, y: 0 },
    },
    transition: {
      duration: 0.16,
      ease: MOTION_EASE,
    },
  },
} as const;

export const REDUCED_SECTION_VARIANTS = {
  hidden: { opacity: 1, y: 0 },
  visible: { opacity: 1, y: 0 },
};

export const REDUCED_SECTION_TRANSITION = {
  duration: 0.01,
  ease: "linear" as const,
};

export const getStaggerDelay = (index = 0): number => index * STAGGER_DELAY_STEP;
