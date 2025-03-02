#include <iostream>


#include <artec/sdk/capturing/IScanner.h>
#include <artec/sdk/capturing/ScannerInfo.h>
#include <artec/sdk/capturing/IArrayScannerId.h>
#include <artec/sdk/capturing/IFrameProcessor.h>
#include <artec/sdk/capturing/IFrame.h>
#include <artec/sdk/base/BaseSdkDefines.h>
#include <artec/sdk/base/Log.h>
#include <artec/sdk/base/io/ObjIO.h>
#include <artec/sdk/base/IFrameMesh.h>
#include <artec/sdk/base/TArrayRef.h>
#include <artec/sdk/base/TRef.h>
#include <artec/sdk/base/Errors.h>
// #include <mutex>
// std::mutex mtx;
using namespace std;

namespace asdk {
    using namespace artec::sdk::base;
    using namespace artec::sdk::capturing;
};
using asdk::TRef;
using asdk::TArrayRef;

int main()
{
    cout << "Starting scanner enumeration..." << endl;

    TRef<asdk::IArrayScannerId> scannersList;
    TRef<asdk::IScanner> scanner;
 asdk::setOutputLevel( asdk::VerboseLevel_Trace );
   asdk::ErrorCode ec = asdk::ErrorCode_OK;

   ec = asdk::enumerateScanners( &scannersList );
    if( ec != asdk::ErrorCode_OK )
    {
        std::wcout << L"failed" << std::endl;
         system("pause"); // Pause the console window
        return 1;
    }
    std::wcout << L"done" << std::endl;

int scanner_count = scannersList->getSize();
    if( scanner_count == 0 )
    {
        std::wcout << L"No scanners found" << std::endl;
           system("pause");
        return 3;
    }
    const asdk::ScannerId* idArray = scannersList->getPointer();
    const asdk::ScannerId& defaultScanner = idArray[0]; // just take the first available scanner
    std::wcout
        << L"Connecting to " << asdk::getScannerTypeName( defaultScanner.type )
        << L" scanner " << defaultScanner.serial << L"... "
    ;

    // TRef<asdk::IScanner> scanner;
    ec = asdk::createScanner( &scanner, &defaultScanner );
    if( ec != asdk::ErrorCode_OK )
    {
        std::wcout << L"failed 2" << std::endl;
   system("pause");
        return 2;
    }
    std::wcout << L"done" << std::endl;
    std::wcout << L"Capturing frame... ";

    TRef<asdk::IFrame> frame;
    TRef<asdk::IFrameMesh> mesh;
    TRef<asdk::IFrameProcessor> processor;
    ec = scanner->createFrameProcessor( &processor );
    if( ec == asdk::ErrorCode_OK )
    {
        frame = NULL;
        ec = scanner->capture( &frame, true ); // with texture
        if( ec == asdk::ErrorCode_OK )
        {
            mesh = NULL;
            ec = processor->reconstructAndTexturizeMesh( &mesh, frame );
            if( ec == asdk::ErrorCode_OK )
            {
                std::wcout << L"done" << std::endl;
                // save the mesh
                ec = asdk::io::Obj::save( L"frame.obj", mesh ); // save in text format
                // working with normals
                // 1. generate normals
                mesh->calculate( asdk::CM_Normals );
                // 2. get normals array using helper class
                asdk::TArrayPoint3F pointsNormals  = mesh->getPointsNormals();
                // 3. get number of normals
                int normalCount = pointsNormals.size();
                ASDK_UNUSED(normalCount);
                // 4. use normal
                asdk::Point3F point = pointsNormals[0];
                ASDK_UNUSED(point);
                std::wcout << L"Captured mesh saved to disk" << std::endl;
            }
            else
            {
                std::wcout << L"failed" << std::endl;
            }
        }
    }
    scanner = NULL;
    std::wcout << L"Scanner released" << std::endl;

    //return 1;
      std::cout << "Press any key to exit...";
    system("pause"); // Pause the console window

    return 0;
}