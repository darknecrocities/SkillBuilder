import React, { useState, useRef, useEffect } from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export const AccessibleModal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
}) => {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };

    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
      modalRef.current?.focus();
    }
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div
        ref={modalRef}
        tabIndex={-1}
        className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl focus:outline-none dark:bg-neutral-900"
      >
        <div className="flex items-center justify-between border-b pb-3">
          <h2 id="modal-title" className="text-lg font-semibold text-neutral-900 dark:text-neutral-100">
            {title}
          </h2>
          <button
            onClick={onClose}
            aria-label="Close modal"
            className="rounded p-1 text-neutral-500 hover:bg-neutral-100 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:hover:bg-neutral-800"
          >
            ✕
          </button>
        </div>
        <div className="mt-4">{children}</div>
      </div>
    </div>
  );
};
