import { NextRequest, NextResponse } from 'next/server';
import { extractLabelsFromXML, analyzeLabels } from '@/lib/xmlAnalyzer';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;
    
    if (!file) {
      return NextResponse.json(
        { success: false, error: 'No file provided' },
        { status: 400 }
      );
    }
    
    if (!file.name.endsWith('.xml')) {
      return NextResponse.json(
        { success: false, error: 'Invalid file type. Please upload an XML file.' },
        { status: 400 }
      );
    }
    
    const content = await file.text();
    
    if (content.length === 0) {
      return NextResponse.json(
        { success: false, error: 'File is empty' },
        { status: 400 }
      );
    }
    
    const labels = await extractLabelsFromXML(content);
    
    if (labels.length === 0) {
      return NextResponse.json(
        { success: false, error: 'No valid labels found in the diagram' },
        { status: 400 }
      );
    }
    
    const analysis = analyzeLabels(labels);
    
    return NextResponse.json({
      success: true,
      data: analysis
    });
    
  } catch (error: any) {
    console.error('Analysis error:', error);
    return NextResponse.json(
      {
        success: false,
        error: error.message || 'Failed to analyze file. Please try again.'
      },
      { status: 500 }
    );
  }
}
