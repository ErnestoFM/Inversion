import { PrismaClient, UserRole, UserStatus, SpaceType, ItemCategory, ItemStatus, EventType, EventVisibility, RequestStatus } from '@prisma/client';
import argon2 from 'argon2';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Iniciando seed de datos para SIGRE — CUTonalá...');

  // Hash estándar para usuarios de prueba en desarrollo: "Cutonala2026!"
  const defaultPasswordHash = await argon2.hash('Cutonala2026!');

  // 1. Limpieza preventiva en orden inverso de dependencias
  console.log('🧹 Limpiando registros previos...');
  await prisma.review.deleteMany();
  await prisma.eventAttendee.deleteMany();
  await prisma.eventCoResponsible.deleteMany();
  await prisma.incident.deleteMany();
  await prisma.loanItem.deleteMany();
  await prisma.loanRequest.deleteMany();
  await prisma.event.deleteMany();
  await prisma.inventoryItem.deleteMany();
  await prisma.space.deleteMany();
  await prisma.notification.deleteMany();
  await prisma.activationToken.deleteMany();
  await prisma.refreshToken.deleteMany();
  await prisma.user.deleteMany();

  // 2. Usuarios Base Institucionales
  console.log('👥 Creando usuarios institucionales del CUTonalá...');
  const admin = await prisma.user.create({
    data: {
      email: 'admin.sigre@udg.mx',
      fullName: 'Coordinación General de Tecnologías',
      studentCode: 'ADMIN-CUT-001',
      role: UserRole.SUPERADMIN,
      status: UserStatus.ACTIVO,
      passwordHash: defaultPasswordHash,
      reputationScore: 100
    }
  });

  const almacenAdmin = await prisma.user.create({
    data: {
      email: 'almacen.ingenierias@cutonala.udg.mx',
      fullName: 'Ing. Roberto Velázquez (Técnico de Almacén)',
      studentCode: 'TEC-ALM-002',
      role: UserRole.ALMACEN_ADMIN,
      status: UserStatus.ACTIVO,
      passwordHash: defaultPasswordHash,
      reputationScore: 100
    }
  });

  const difusionAdmin = await prisma.user.create({
    data: {
      email: 'cineteca.difusion@cutonala.udg.mx',
      fullName: 'Lic. Mariana Solís (Coordinación de Extensión y Cineteca)',
      studentCode: 'EXT-CIN-003',
      role: UserRole.DIFUSION_EVENTOS,
      status: UserStatus.ACTIVO,
      passwordHash: defaultPasswordHash,
      reputationScore: 100
    }
  });

  const docente = await prisma.user.create({
    data: {
      email: 'elizabeth.hernandez@udg.mx',
      fullName: 'Mtra. Elizabeth Cristina Hernández Hernández',
      studentCode: 'DOC-UDG-2045',
      career: 'Ingeniería en Ciencias Computacionales',
      role: UserRole.DOCENTE,
      status: UserStatus.ACTIVO,
      passwordHash: defaultPasswordHash,
      reputationScore: 100
    }
  });

  const estudiante1 = await prisma.user.create({
    data: {
      email: 'ernesto.fierro@alumnos.udg.mx',
      fullName: 'Ernesto Hatuey Fierro Meléndez',
      studentCode: '219483721',
      career: 'Ingeniería en Ciencias Computacionales',
      semester: 8,
      role: UserRole.ESTUDIANTE,
      status: UserStatus.ACTIVO,
      passwordHash: defaultPasswordHash,
      reputationScore: 100
    }
  });

  const estudiante2 = await prisma.user.create({
    data: {
      email: 'carlos.barragan@alumnos.udg.mx',
      fullName: 'Carlos Emiliano Barragán Padilla',
      studentCode: '218392104',
      career: 'Ingeniería en Ciencias Computacionales',
      semester: 8,
      role: UserRole.ESTUDIANTE,
      status: UserStatus.ACTIVO,
      passwordHash: defaultPasswordHash,
      reputationScore: 100
    }
  });

  // 3. Catálogo de Espacios Físicos del CUTonalá
  console.log('🏢 Creando catálogo de espacios físicos...');
  const cineteca = await prisma.space.create({
    data: {
      name: 'Cineteca CUTonalá',
      code: 'ESP-CINETECA-01',
      type: SpaceType.CINETECA,
      building: 'Edificio de Biblioteca Central (Nivel 2)',
      capacity: 120,
      hasProjector: true,
      hasAudio: true,
      rulesText: 'Prohibido introducir alimentos grasos o bebidas sin tapa. Mantener apagados teléfonos móviles.'
    }
  });

  const auditorioA = await prisma.space.create({
    data: {
      name: 'Auditorio Principal de Ingenierías',
      code: 'ESP-AUDITORIO-A',
      type: SpaceType.AUDITORIO,
      building: 'Edificio A (Planta Baja)',
      capacity: 320,
      hasProjector: true,
      hasAudio: true,
      rulesText: 'Uso exclusivo para conferencias magistrales, congresos académicos y presentaciones de titulación.'
    }
  });

  const labComputo = await prisma.space.create({
    data: {
      name: 'Laboratorio de Cómputo Especializado e IA',
      code: 'ESP-LAB-COMP-01',
      type: SpaceType.LABORATORIO,
      building: 'Edificio B (Planta Alta)',
      capacity: 40,
      hasProjector: true,
      hasAudio: false,
      rulesText: 'Requiere bata blanca de laboratorio. Prohibida la instalación de software no autorizado sin permiso del encargado.'
    }
  });

  const aulaMagna = await prisma.space.create({
    data: {
      name: 'Aula Magna Multidisciplinaria A-101',
      code: 'ESP-AULA-A101',
      type: SpaceType.AULA,
      building: 'Edificio A (Primer Nivel)',
      capacity: 65,
      hasProjector: true,
      hasAudio: true,
      rulesText: 'Horario de uso académico de 08:00 a 19:00 hrs.'
    }
  });

  // 4. Catálogo de Recursos y Materiales de Almacén
  console.log('📦 Creando inventario de materiales y equipo...');
  await prisma.inventoryItem.createMany({
    data: [
      {
        name: 'Laptop Lenovo ThinkPad T14 Gen 4 (Core i7 / 32GB RAM)',
        assetTag: 'UDG-CUT-INV-00101',
        serialNumber: 'SN-THINK-T14-001',
        category: ItemCategory.COMPUTO,
        brand: 'Lenovo',
        model: 'ThinkPad T14',
        status: ItemStatus.DISPONIBLE,
        estimatedLifespanHours: 5000,
        rulesText: 'Equipo para desarrollo y proyectos modulares. Préstamo extendido requiere visto bueno de Coordinación.'
      },
      {
        name: 'Laptop Lenovo ThinkPad T14 Gen 4 (Core i7 / 32GB RAM)',
        assetTag: 'UDG-CUT-INV-00102',
        serialNumber: 'SN-THINK-T14-002',
        category: ItemCategory.COMPUTO,
        brand: 'Lenovo',
        model: 'ThinkPad T14',
        status: ItemStatus.DISPONIBLE,
        estimatedLifespanHours: 5000
      },
      {
        name: 'Proyector Láser Epson PowerLite L520U (5200 Lúmenes)',
        assetTag: 'UDG-CUT-INV-00201',
        serialNumber: 'SN-EPSON-L520-001',
        category: ItemCategory.PROYECCION,
        brand: 'Epson',
        model: 'PowerLite L520U',
        status: ItemStatus.DISPONIBLE,
        estimatedLifespanHours: 20000
      },
      {
        name: 'Kit de Micrófonos Inalámbricos Shure BLX288/PG58 Dual',
        assetTag: 'UDG-CUT-INV-00301',
        serialNumber: 'SN-SHURE-MIC-001',
        category: ItemCategory.AUDIO,
        brand: 'Shure',
        model: 'BLX288',
        status: ItemStatus.DISPONIBLE,
        estimatedLifespanHours: 8000
      },
      {
        name: 'Kit de Sensores y Robótica Arduino Mega 2560 Pro',
        assetTag: 'UDG-CUT-INV-00401',
        serialNumber: 'SN-ARDUINO-MEGA-001',
        category: ItemCategory.HERRAMIENTAS,
        brand: 'Arduino Official',
        model: 'Mega 2560',
        status: ItemStatus.DISPONIBLE,
        estimatedLifespanHours: 3000
      },
      {
        name: 'Adaptador Multipuerto USB-C a HDMI 4K / USB 3.0',
        assetTag: 'UDG-CUT-INV-00501',
        serialNumber: 'SN-ADAPT-USBC-001',
        category: ItemCategory.CABLEADO_ADAPTADORES,
        brand: 'UGreen',
        model: 'CM511',
        status: ItemStatus.DISPONIBLE,
        estimatedLifespanHours: 2000
      }
    ]
  });

  // 5. Evento Cartelera de Cineteca (Prueba inicial)
  console.log('🎬 Creando función inicial de la Cineteca...');
  const nextWeekDate = new Date();
  nextWeekDate.setDate(nextWeekDate.getDate() + 5);
  nextWeekDate.setHours(16, 0, 0, 0);

  const nextWeekEndDate = new Date(nextWeekDate);
  nextWeekEndDate.setHours(18, 30, 0, 0);

  await prisma.event.create({
    data: {
      title: 'Muestra de Cine Mexicano: Macario (1960)',
      description: 'Clásico restaurado del cine de oro mexicano dirigido por Roberto Gavaldón y fotografía de Gabriel Figueroa. Función con cupo limitado y debate posterior con la academia de Humanidades.',
      type: EventType.CINETECA,
      visibility: EventVisibility.PUBLICO,
      spaceId: cineteca.id,
      startTime: nextWeekDate,
      endTime: nextWeekEndDate,
      maxCapacity: 120,
      status: RequestStatus.APROBADO,
      posterUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Macario_%281960%29_poster.jpg/440px-Macario_%281960%29_poster.jpg',
      trailerUrl: 'https://www.youtube.com/watch?v=kYJv0y9vO3M',
      creatorId: difusionAdmin.id
    }
  });

  console.log('✅ Seed completado exitosamente con cuentas y catálogos de CUTonalá.');
  console.log('──────────────────────────────────────────────────────────');
  console.log('Credenciales de prueba generadas (Contraseña: Cutonala2026!):');
  console.log('  - SuperAdmin: admin.sigre@udg.mx');
  console.log('  - Almacén/Técnico: almacen.ingenierias@cutonala.udg.mx');
  console.log('  - Difusión/Cineteca: cineteca.difusion@cutonala.udg.mx');
  console.log('  - Docente: elizabeth.hernandez@udg.mx');
  console.log('  - Alumno 1: ernesto.fierro@alumnos.udg.mx (Reputación: 100)');
  console.log('  - Alumno 2: carlos.barragan@alumnos.udg.mx (Reputación: 100)');
  console.log('──────────────────────────────────────────────────────────');
}

main()
  .catch((e) => {
    console.error('❌ Error durante la ejecución del seed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
