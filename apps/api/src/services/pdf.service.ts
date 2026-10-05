import PDFDocument from 'pdfkit';
import fs from 'fs';
import path from 'path';

export interface ResponsivaPdfData {
  folioNumber: string;
  createdAt: string;
  userName: string;
  studentCode: string;
  career?: string;
  purpose: string;
  spaceName?: string;
  items: {
    name: string;
    assetTag: string;
    serialNumber: string;
  }[];
  coResponsibles: {
    fullName: string;
    studentCode: string;
    signedAt?: string;
  }[];
  requesterSignatureBase64?: string;
  approverSignatureBase64?: string;
  approverName?: string;
  ipAddress?: string;
}

export class PdfService {
  static async generateResponsivaPdf(data: ResponsivaPdfData, outputDirectory: string): Promise<string> {
    if (!fs.existsSync(outputDirectory)) {
      fs.mkdirSync(outputDirectory, { recursive: true });
    }

    const fileName = `responsiva_${data.folioNumber.replace(/[^a-zA-Z0-9_-]/g, '_')}.pdf`;
    const filePath = path.join(outputDirectory, fileName);

    return new Promise((resolve, reject) => {
      const doc = new PDFDocument({ margin: 40, size: 'A4' });
      const stream = fs.createWriteStream(filePath);

      doc.pipe(stream);

      // --- Encabezado Oficial ---
      doc
        .fontSize(18)
        .fillColor('#1e3a8a')
        .text('CENTRO UNIVERSITARIO DE TONALÁ', { align: 'center' });
      doc
        .fontSize(12)
        .fillColor('#475569')
        .text('Universidad de Guadalajara — SIGRE', { align: 'center' });
      doc.moveDown(0.5);
      doc
        .fontSize(14)
        .fillColor('#0f172a')
        .text(`ACTA RESPONSIVA DE PRÉSTAMO / USO DE ESPACIOS — FOLIO: ${data.folioNumber}`, {
          align: 'center',
          underline: true
        });
      doc.moveDown(1);

      // --- Datos del Solicitante ---
      doc.fontSize(10).fillColor('#000000');
      doc.text(`Fecha y Hora de Emisión: ${new Date(data.createdAt).toLocaleString('es-MX')}`);
      doc.text(`Solicitante Titular: ${data.userName} (Código: ${data.studentCode})`);
      if (data.career) doc.text(`Carrera / Adscripción: ${data.career}`);
      if (data.ipAddress) doc.text(`IP de Registro y Aceptación Digital: ${data.ipAddress}`);
      doc.text(`Motivo / Propósito: ${data.purpose}`);
      if (data.spaceName) doc.text(`Espacio Asignado: ${data.spaceName}`);

      doc.moveDown(1);

      // --- Lista de Materiales e Insumos ---
      doc.fontSize(11).fillColor('#1e3a8a').text('1. MATERIALES Y EQUIPOS ASIGNADOS:');
      doc.fontSize(10).fillColor('#000000');

      if (data.items.length === 0) {
        doc.text('  * Ningún material de inventario adicional solicitado.');
      } else {
        data.items.forEach((item, idx) => {
          doc.text(`  ${idx + 1}. ${item.name} | Placa: ${item.assetTag} | Serie: ${item.serialNumber}`);
        });
      }

      doc.moveDown(1);

      // --- Co-Responsables ---
      if (data.coResponsibles && data.coResponsibles.length > 0) {
        doc.fontSize(11).fillColor('#1e3a8a').text('2. CO-RESPONSABLES REGISTRADOS:');
        doc.fontSize(10).fillColor('#000000');
        data.coResponsibles.forEach((cr, idx) => {
          const signStatus = cr.signedAt ? `[Firmado: ${new Date(cr.signedAt).toLocaleDateString()}]` : '[Pendiente de firma]';
          doc.text(`  ${idx + 1}. ${cr.fullName} (Código: ${cr.studentCode}) — ${signStatus}`);
        });
        doc.moveDown(1);
      }

      // --- Cláusulas y Normativa ---
      doc.fontSize(11).fillColor('#1e3a8a').text('3. TÉRMINOS, CONDICIONES Y RESPONSABILIDAD:');
      doc
        .fontSize(8.5)
        .fillColor('#334155')
        .text(
          'El titular y los co-responsables declaran recibir el equipo y/o instalaciones en óptimas condiciones de funcionamiento. ' +
          'Se comprometen a hacer uso exclusivo para los fines académicos autorizados y a devolverlos en la fecha y hora convenidas. ' +
          'En caso de daño parcial, negligencia, descompostura o extravío, se obligan a participar en el proceso de Reparación de Daños Supervisada ' +
          'por la Coordinación de Almacén y Servicios Generales de CUTonalá, asumiendo los costos de reposición o reparación correspondientes.',
          { align: 'justify' }
        );

      doc.moveDown(2);

      // --- Firmas Digitales ---
      doc.fontSize(10).fillColor('#000000');
      const ySign = doc.y;

      // Columna Izquierda: Solicitante
      doc.text('____________________________________', 60, ySign);
      doc.text(`Firma del Solicitante: ${data.userName}`, 60, ySign + 15);
      doc.text(`Código: ${data.studentCode}`, 60, ySign + 28);
      doc.text('[Aceptación y Firma Digital Validada]', 60, ySign + 40);

      // Columna Derecha: Administrador / Almacén
      doc.text('____________________________________', 330, ySign);
      doc.text(`Firma de Almacén / Administración`, 330, ySign + 15);
      doc.text(data.approverName ? `Autorizado por: ${data.approverName}` : 'Responsable de Espacios CUTonalá', 330, ySign + 28);
      doc.text('[Autorización Oficial en Plataforma]', 330, ySign + 40);

      doc.end();

      stream.on('finish', () => resolve(filePath));
      stream.on('error', (err) => reject(err));
    });
  }
}
