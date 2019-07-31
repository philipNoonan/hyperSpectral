//#version 430

//layout(local_size_x = 32, local_size_y = 32, local_size_z = 1) in;

//// images
//layout(binding = 0, r8ui) uniform uimage3D volumeData;
//layout(binding = 1, r8ui) uniform uimage3D volumeDataOutput;











//void main()
//{
//    ivec3 writePos = ivec3(gl_GlobalInvocationID.xyz);
//    ivec3 readPos = writePos * 2;
//    ivec3 imSize = ivec3(0);

//    if (baseLevel == 1)
//    {
//        imSize = imageSize(histoPyramidBaseLevel);
//    }
//    else if (baseLevel == 0)
//    {
//        imSize = imageSize(volumeData);
//    }
//    if (readPos.x > imSize.x || readPos.y > imSize.y || readPos.z > imSize.z)
//    {
//        return false;
//    }

//    uint writeValue = 0;
//    if (baseLevel == 1)
//    {
//        writeValue = imageLoad(histoPyramidBaseLevel, readPos).x +
//                         imageLoad(histoPyramidBaseLevel, readPos + ivec3(cubeOffsets[1].xyz)).x +
//                         imageLoad(histoPyramidBaseLevel, readPos + ivec3(cubeOffsets[2].xyz)).x +
//                         imageLoad(histoPyramidBaseLevel, readPos + ivec3(cubeOffsets[3].xyz)).x +

//                         imageLoad(histoPyramidBaseLevel, readPos + ivec3(cubeOffsets[4].xyz)).x +
//                         imageLoad(histoPyramidBaseLevel, readPos + ivec3(cubeOffsets[5].xyz)).x +
//                         imageLoad(histoPyramidBaseLevel, readPos + ivec3(cubeOffsets[6].xyz)).x +
//                         imageLoad(histoPyramidBaseLevel, readPos + ivec3(cubeOffsets[7].xyz)).x;
//    }
//    else if (baseLevel == 0)
//    {
//        writeValue = imageLoad(volumeData, readPos).x +
//                         imageLoad(volumeData, readPos + ivec3(cubeOffsets[1].xyz)).x +
//                         imageLoad(volumeData, readPos + ivec3(cubeOffsets[2].xyz)).x +
//                         imageLoad(volumeData, readPos + ivec3(cubeOffsets[3].xyz)).x +

//                         imageLoad(volumeData, readPos + ivec3(cubeOffsets[4].xyz)).x +
//                         imageLoad(volumeData, readPos + ivec3(cubeOffsets[5].xyz)).x +
//                         imageLoad(volumeData, readPos + ivec3(cubeOffsets[6].xyz)).x +
//                         imageLoad(volumeData, readPos + ivec3(cubeOffsets[7].xyz)).x;
//    }



//    imageStore(volumeDataOutput, writePos, uvec4(writeValue));
//}