export interface ValidationResult {
  valid: boolean;
  error?: string;
}

export class CutonalaBusinessRules {
  /**
   * Valida si un horario está dentro de los días y horas de operación del CUTonalá
   * Lunes a Sábado de 08:00 a 19:00 hrs. Domingos cerrado.
   */
  public static validateOperatingHours(startTime: Date, endTime: Date): ValidationResult {
    if (endTime <= startTime) {
      return { valid: false, error: 'La hora de finalización debe ser posterior a la de inicio.' };
    }

    const startDay = startTime.getDay(); // 0 = Domingo, 1-6 = Lunes a Sábado
    const endDay = endTime.getDay();

    if (startDay === 0 || endDay === 0) {
      return { valid: false, error: 'El Centro Universitario no opera servicios de préstamo ni reserva en domingos.' };
    }

    const startHour = startTime.getHours() + startTime.getMinutes() / 60;
    const endHour = endTime.getHours() + endTime.getMinutes() / 60;

    if (startHour < 8.0 || endHour > 19.0) {
      return {
        valid: false,
        error: 'El horario de servicio para espacios y préstamos es exclusivamente de 08:00 a 19:00 hrs.'
      };
    }

    return { valid: true };
  }

  /**
   * Valida la ventana de antelación obligatoria para espacios:
   * Mínimo 3 días (72 hrs) para preparación/logística, máximo 15 días naturales.
   */
  public static validateSpaceAnticipation(startTime: Date, now: Date = new Date()): ValidationResult {
    const diffMs = startTime.getTime() - now.getTime();
    const diffHours = diffMs / (1000 * 60 * 60);
    const diffDays = diffMs / (1000 * 60 * 60 * 24);

    if (diffHours < 72) {
      return {
        valid: false,
        error: 'Las reservaciones de espacios requieren al menos 3 días (72 hrs) de anticipación para logística y montaje.'
      };
    }

    if (diffDays > 15) {
      return {
        valid: false,
        error: 'No se permite reservar espacios con más de 15 días naturales de anticipación.'
      };
    }

    return { valid: true };
  }

  /**
   * Valida el periodo de préstamo de materiales:
   * Ordinario: Máximo 3 días (72 hrs)
   * Extendido: Hasta 30 días (1 mes) condicionado a permiso especial
   */
  public static validateLoanDuration(startTime: Date, endTime: Date, isExtendedLoan: boolean = false): ValidationResult {
    const durationMs = endTime.getTime() - startTime.getTime();
    const durationDays = durationMs / (1000 * 60 * 60 * 24);

    if (durationDays <= 0) {
      return { valid: false, error: 'El periodo de préstamo debe ser mayor a 0 horas.' };
    }

    if (!isExtendedLoan && durationDays > 3) {
      return {
        valid: false,
        error: 'El préstamo estándar no puede exceder 3 días (72 hrs). Para proyectos o laptops solicita Préstamo Extendido con visto bueno de Coordinación.'
      };
    }

    if (isExtendedLoan && durationDays > 30) {
      return {
        valid: false,
        error: 'El préstamo extendido no puede superar el límite máximo de 30 días naturales (1 mes).'
      };
    }

    return { valid: true };
  }
}
