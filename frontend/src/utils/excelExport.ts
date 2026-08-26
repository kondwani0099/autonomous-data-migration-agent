/**
 * Dependency-free Excel export utility.
 *
 * Generates a Microsoft Excel-compatible workbook (XML Spreadsheet 2003, .xls)
 * from an array of plain records and triggers a browser download. The
 * `<?mso-application progid="Excel.Sheet"?>` declaration tells Excel to open
 * the file natively as a spreadsheet, so no external libraries are required.
 */

export interface ExcelColumn {
  key: string;
  label: string;
}

export interface ExportOptions {
  fileName: string;
  sheetName?: string;
  columns?: ExcelColumn[];
}

function escapeXml(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function cellValue(value: unknown): { type: 'Number' | 'String'; text: string } {
  if (typeof value === 'number' && Number.isFinite(value)) {
    return { type: 'Number', text: String(value) };
  }
  return { type: 'String', text: escapeXml(String(value ?? '')) };
}

function buildWorkbookXml(
  sheetName: string,
  columns: ExcelColumn[],
  rows: Record<string, unknown>[],
): string {
  const headerCells = columns
    .map((c) => `<Cell ss:StyleID="Header"><Data ss:Type="String">${escapeXml(c.label)}</Data></Cell>`)
    .join('');

  const dataRows = rows
    .map((row) => {
      const cells = columns
        .map((c) => {
          const { type, text } = cellValue(row[c.key]);
          return `<Cell><Data ss:Type="${type}">${text}</Data></Cell>`;
        })
        .join('');
      return `<Row>${cells}</Row>`;
    })
    .join('');

  return `<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:html="http://www.w3.org/TR/REC-html40">
<Styles>
<Style ss:ID="Default" ss:Name="Normal"><Alignment ss:Vertical="Bottom"/><Font ss:FontName="Calibri" ss:Size="11"/></Style>
<Style ss:ID="Header"><Font ss:Bold="1"/><Interior ss:Color="#EEF2FF" ss:Pattern="Solid"/></Style>
</Styles>
<Worksheet ss:Name="${sheetName}">
<Table>
${headerRowXml(headerCells)}
${dataRows}
</Table>
</Worksheet>
</Workbook>`;
}

function headerRowXml(headerCells: string): string {
  if (!headerCells) return '';
  return `<Row>${headerCells}</Row>`;
}

/**
 * Export rows of data to an Excel-compatible .xls file and trigger a download.
 */
export function exportToExcel(
  rows: Record<string, unknown>[],
  options: ExportOptions,
): void {
  const sheetName = (options.sheetName || 'Sheet1')
    .slice(0, 31)
    .replace(/[\\/?*[\]]/g, ' ');

  const columns: ExcelColumn[] =
    options.columns && options.columns.length > 0
      ? options.columns
      : rows.length > 0
        ? Object.keys(rows[0]).map((key) => ({ key, label: key }))
        : [];

  const xml = buildWorkbookXml(sheetName, columns, rows);
  const blob = new Blob([xml], { type: 'application/vnd.ms-excel' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = `${options.fileName}.xls`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
