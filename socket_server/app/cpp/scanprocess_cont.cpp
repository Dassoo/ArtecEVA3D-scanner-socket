#undef NDEBUG
#include <windows.h> // Include for GetAsyncKeyState and VK_SPACE
#include <string>
#include <iostream>
#include <fstream>
#include <ctime>
#include <sstream>
#include <cwchar>
#include <cstdlib>
#include <cstdio>
#include <filesystem>
#include <chrono>
#include <vector>
#include <thread>
#include <atomic>
#include <mutex>
#include <condition_variable>
#include <artec/sdk/capturing/IScanner.h>
#include <artec/sdk/capturing/IArrayScannerId.h>
#include <artec/sdk/capturing/IFrameProcessor.h>
#include <artec/sdk/capturing/IFrame.h>
#include <artec/sdk/base/BaseSdkDefines.h>
#include <artec/sdk/base/Log.h>
#include <artec/sdk/base/io/ObjIO.h>
#include <artec/sdk/base/IFrameMesh.h>
#include <artec/sdk/base/TArrayRef.h>

namespace asdk {
    using namespace artec::sdk::base;
    using namespace artec::sdk::capturing;
};

using asdk::TRef;
using asdk::TArrayRef;

std::atomic<bool> scanningPaused(false);
std::atomic<bool> scanningActive(true);
std::mutex mtx;
std::condition_variable cv;
std::vector<TRef<asdk::IFrameMesh>> meshes;
bool newFrameAvailable = false;

void monitorKeyPress() {
    while (scanningActive) {
        if (GetAsyncKeyState('P') & 0x8000) { // Check if 'p' key is pressed
            scanningPaused = !scanningPaused; // Toggle pause state
            // std::this_thread::sleep_for(std::chrono::milliseconds(100)); // Debounce delay
        }
        if (GetAsyncKeyState('Q') & 0x8000) { // Check if 'q' key is pressed
            scanningActive = false; // Stop scanning
            // std::this_thread::sleep_for(std::chrono::milliseconds(100)); // Debounce delay
        }
        // std::this_thread::sleep_for(std::chrono::milliseconds(100)); // Polling interval
    }
}

void processFrames() {
    while (scanningActive) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [] { return newFrameAvailable; });

        // Process captured frames
        for (const auto& mesh : meshes) {
            // Just mark new frames available, actual saving will be done in main thread later.
        }
        
        newFrameAvailable = false; // Reset flag
    }
}

void saveMeshes(const std::string& outputDir) {
    for (const auto& mesh : meshes) {
        // Get current time in milliseconds for filename
        auto now = std::chrono::system_clock::now();
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();

        std::wstringstream wss;
        wss << outputDir.c_str() << L"frame_" << ms << L".obj"; // Use timestamp as filename
        std::wstring filename = wss.str();

        asdk::ErrorCode ec = asdk::io::Obj::save(filename.c_str(), mesh);
        if (ec == asdk::ErrorCode_OK) {
            std::wcout << L"Captured mesh saved to disk: " << filename << std::endl;
        } else {
            std::wcout << L"Failed to save mesh." << std::endl;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 1) {
        std::cout << "Error: Missing output path argument." << std::endl;
        return 1;
    }

    // Use the first command line argument as the output directory
    std::string outputDir = std::string(argv[1]) + "\\";
    std::cout << "Output directory: " << outputDir << std::endl;

    // Create the output directory if it doesn't exist
    std::filesystem::create_directory(outputDir);

    asdk::setOutputLevel(asdk::VerboseLevel_Trace);
    asdk::ErrorCode ec = asdk::ErrorCode_OK;
    TRef<asdk::IArrayScannerId> scannersList;

    std::wcout << L"Enumerating scanners... ";
    ec = asdk::enumerateScanners(&scannersList);
    
    if (ec != asdk::ErrorCode_OK) {
        std::wcout << L"failed" << std::endl;
        return 1;
    }
    
    std::wcout << L"done" << std::endl;

    int scanner_count = scannersList->getSize();
    
    if (scanner_count == 0) {
        std::wcout << L"No scanners found" << std::endl;
        return 3;
    }

    const asdk::ScannerId* idArray = scannersList->getPointer();
    const asdk::ScannerId& defaultScanner = idArray[0]; // just take the first available scanner

    std::wcout 
        << L"Connecting to " << asdk::getScannerTypeName(defaultScanner.type) 
        << L" scanner " << defaultScanner.serial << L"... ";
        
    TRef<asdk::IScanner> scanner;
    
    ec = asdk::createScanner(&scanner, &defaultScanner);
    
    if (ec != asdk::ErrorCode_OK) {
        std::wcout << L"failed" << std::endl;
        return 2;
    }
    
    std::wcout << L"done" << std::endl;

    // Start monitoring key presses in a separate thread
    std::thread keyPressThread(monitorKeyPress);
    
    while (scanningActive) {
        if (!scanningPaused) {
            std::wcout << L"Capturing frame... ";
            TRef<asdk::IFrame> frame;
            TRef<asdk::IFrameProcessor> processor;

            ec = scanner->createFrameProcessor(&processor);
            
            if (ec == asdk::ErrorCode_OK) {
                frame = NULL;
                ec = scanner->capture(&frame, true); // with texture
                
                if (ec == asdk::ErrorCode_OK) {
                    TRef<asdk::IFrameMesh> mesh;
                    ec = processor->reconstructAndTexturizeMesh(&mesh, frame);
                    
                    if (ec == asdk::ErrorCode_OK) {
                        {
                            std::lock_guard<std::mutex> lock(mtx);
                            meshes.push_back(mesh); // Store the captured mesh
                            newFrameAvailable = true; // Signal that a new frame is available
                        }
                        cv.notify_one(); // Notify processing thread
                        std::wcout << L"done." << std::endl; 
                    } else {
                        std::wcout << L"failed to reconstruct mesh." << std::endl; 
                    }
                } else {
                    std::wcout << L"failed to capture frame." << std::endl; 
                }
            } else {
                std::wcout << L"failed to create frame processor." << std::endl; 
            }
        } else {
            // Sleep while paused to reduce CPU usage
            std::this_thread::sleep_for(std::chrono::milliseconds(100)); 
        }

        // Optional: Add a small delay between captures to avoid overwhelming the scanner
        std::this_thread::sleep_for(std::chrono::milliseconds(10)); 
    }

    keyPressThread.join();   // Wait for key press thread to finish

    // Save all captured meshes to the output directory after exiting scanning loop
    saveMeshes(outputDir);

    return 0;
}