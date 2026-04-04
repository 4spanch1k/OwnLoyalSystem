import { CSSProperties, ReactNode } from "react";
import { motion, useReducedMotion } from "motion/react";
import {
  getStaggerDelay,
  REDUCED_SECTION_TRANSITION,
  REDUCED_SECTION_VARIANTS,
  SECTION_MOTION_PRESETS,
} from "../../services/motionPresets";

type FadeUpVariant = keyof typeof SECTION_MOTION_PRESETS;

interface Props {
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
  index?: number;
  variant?: FadeUpVariant;
}

export function FadeUpSection({
  children,
  className,
  style,
  index = 0,
  variant = "section",
}: Props) {
  const reduceMotion = useReducedMotion();
  const preset = SECTION_MOTION_PRESETS[variant];

  return (
    <motion.div
      className={className}
      style={reduceMotion ? style : { ...style, willChange: "transform, opacity" }}
      initial="hidden"
      animate="visible"
      variants={reduceMotion ? REDUCED_SECTION_VARIANTS : preset.variants}
      transition={
        reduceMotion
          ? REDUCED_SECTION_TRANSITION
          : { ...preset.transition, delay: getStaggerDelay(index) }
      }
    >
      {children}
    </motion.div>
  );
}
