import { ReactNode } from "react";
import { motion, useReducedMotion } from "motion/react";
import {
  PAGE_TRANSITION,
  PAGE_VARIANTS,
  REDUCED_PAGE_TRANSITION,
  REDUCED_PAGE_VARIANTS,
} from "../../services/motionPresets";

interface Props {
  children: ReactNode;
}

export function AnimatedPage({ children }: Props) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={reduceMotion ? false : "hidden"}
      animate="visible"
      variants={reduceMotion ? REDUCED_PAGE_VARIANTS : PAGE_VARIANTS}
      transition={reduceMotion ? REDUCED_PAGE_TRANSITION : PAGE_TRANSITION}
    >
      {children}
    </motion.div>
  );
}
